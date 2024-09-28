from obstechutils.db import DataBase
from obstechutils.types import TimeType, TimeDeltaType
from obstechutils import logging
from obstechutils.dataclasses import dataclass, Field

from astropy.time import Time
from functools import wraps

# only configured reading the database for coeffs, no calibration
# actually done here

@dataclass(frozen=False,config=dict(validate_default=True))
class PyrgeometerCalibrator:

    """Calibration of a sky IR temperature sensor."""

    id: str    
    db: DataBase
    db_table_name: str
    update_period: TimeDeltaType = '1d'
    coefficients: list[float] = Field(
        default_factory=lambda: [100., 0., 0., 0., 0., 0., 0.],
        min_length=7, max_length=7,
    )
    last_update_time: TimeType = '1980-01-01'
    update_timeout: TimeDeltaType = '1s'

    @classmethod
    def from_credentials(cls, user: str, database: str, **kwargs):

        db = DataBase.from_credentials(database=database, user=user)
        return cls(db=db, **kwargs)
    
    def __getattribute__(self, x):
        if x == 'coefficients':
            self._update()
        return object.__getattribute__(self, x)

    def sky_temperature(
            self, 
            temperature: float, 
            temperature_ir: float
    ) -> float:

        td = self.temperature_correction(temperature)
        return temperature_ir - td

    def temperature_correction(self, temperature: float) -> float:

        K = self.coefficients         
        K1, K2, K3, K4, K5, K6, K7 = [
            K[0]/100, K[1]/10, K[2]/100, K[3]/1000, K[4]/100, K[5]/10, K[6]/100
        ]

        A = abs(K2 - temperature)
        S = np.sign(temperature - K2)

        T67 = sgn(K6) * S * A if A < 1 else K6 * S * np.log10(A) + K7
        Td = K1 * S * A + K3 * exp(K4 * temperature)**K5 + T67

        return Td

    def _update(self):
        
        dt = (now := Time.now()) - self.last_update_time 
        if dt < self.update_period:
            return
            
        sensor = f"sensor {self.id}"
        logger = logging.getLogger('obstechutils')
                
        msg = f'{sensor}: last update is {dt.jd:.0f} days old'
        logger.info(msg)

        try:

            query = f"""
                SELECT k1,k2,k3,k4,k5,k6,k7 
                FROM {self.db_table_name}
                WHERE identifier = '{self.id}'
                ORDER BY id DESC
                LIMIT 1
            """

            t_query = 1000 * self.update_timeout.sec

            with self.db.connect() as conn:
                cursor = conn.cursor()
                cursor.execute("SET SESSION MAX_EXECUTION_TIME={t_query}")
                cursor.execute(query)
                values = cursor.fetchall()

            if not values:
                raise RuntimeError('No data found in database')
            self.coefficients = list(values[0])
            self.last_update_time = now

        except Exception as e:

            msg = f'{sensor}: could not update coefficients: {e}'
            logger.error(msg)

        else:
            msg = f'{sensor}: coefficients updated: {values}'
            logger.info(msg)

if __name__ == "__main__":
    calib = PyrgeometerCalibrator(
        user='generic_obstech', database='ElSauceWeather',
        db_table_name='cloudsensors_params',
        id='aag1'
    )
    print(calib)
