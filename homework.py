from dataclasses import asdict, dataclass


@dataclass
class InfoMessage:
    """Информационное сообщение о тренировке."""
    training_type: str
    duration: float  # hours
    distance: float  # km
    speed: float  # km/h
    calories: float  # Kcal

    message = ('Тип тренировки: {training_type}; Длительность: {duration:.3f} '
               'ч.; Дистанция: {distance:.3f} км; Ср. скорость: {speed:.3f} '
               'км/ч; Потрачено ккал: {calories:.3f}.')

    def get_message(self) -> str:
        return self.message.format(**asdict(self))


@dataclass
class Training:
    """Базовый класс тренировки."""
    LEN_STEP: float = 0.65  # meters
    M_IN_KM: int = 1000  # meters

    def __init__(self, action: int, duration: float, weight: float) -> None:
        self.action = action
        self.duration = duration  # km
        self.weight = weight  # kg

    def get_distance(self) -> float:
        """Получить дистанцию в км."""
        return self.action * self.LEN_STEP / self.M_IN_KM

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения."""
        return self.get_distance() / self.duration

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        pass

    def show_training_info(self) -> InfoMessage:
        """Вернуть информационное сообщение о выполненной тренировке."""
        result: InfoMessage = InfoMessage(type(self).__name__,
                                          self.duration,
                                          self.get_distance(),
                                          self.get_mean_speed(),
                                          self.get_spent_calories())
        return result


class Running(Training):
    """Тренировка: бег."""

    coeff_calorie_1 = 18
    coeff_calorie_2 = 20
    training_time_in_mints = 60  # minutes

    def __init__(self, action: int, duration: float, weight: float) -> None:
        super().__init__(action, duration, weight)

    def get_spent_calories(self) -> float:
        return ((self.coeff_calorie_1 * self.get_mean_speed()
                - self.coeff_calorie_2) * self.weight / self.M_IN_KM
                * (self.duration * self.training_time_in_mints))


class SportsWalking(Training):
    """Тренировка: спортивная ходьба."""

    coeff_calorie_3 = 0.035
    coeff_calorie_4 = 0.029
    training_time_in_mints = 60  # minutes

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 height: float) -> None:
        super().__init__(action, duration, weight)
        self.height = height

    def get_spent_calories(self) -> float:
        return (self.coeff_calorie_3 * self.weight
                + (self.get_mean_speed()**2 // self.height)
                * self.coeff_calorie_4
                * self.weight) * (self.duration * self.training_time_in_mints)


@dataclass
class Swimming(Training):
    """Тренировка: плавание."""
    coeff_calorie_5 = 1.1
    coeff_calorie_6 = 2.0
    LEN_STEP = 1.38  # meters

    def __init__(self, action: int, duration: float, weight: float,
                 length_pool: int, count_pool: int) -> None:
        super().__init__(action, duration, weight)
        self.length_pool = length_pool
        self.count_pool = count_pool

    def get_mean_speed(self):
        return (self.length_pool * self.count_pool / self.M_IN_KM
                / self.duration)

    def get_spent_calories(self) -> float:
        return ((self.get_mean_speed() + self.coeff_calorie_5)
                * self.coeff_calorie_6 * self.weight)


def read_package(workout_type: str, data: list[int]) -> Training:
    """Прочитать данные полученные от датчиков."""
    read: dict = {
        'RUN': Running,
        'WLK': SportsWalking,
        'SWM': Swimming,
    }
    if workout_type not in read.keys():
        raise NameError("Type_Error")
    if workout_type in read.keys():
        workout_class = read[workout_type]
    return workout_class(*data)


def main(training) -> None:
    """Главная функция."""
    info = training.show_training_info()
    print(info.get_message())


if __name__ == '__main__':
    packages = [
        ('SWM', [720, 1, 80, 25, 40]),
        ('RUN', [15000, 1, 75]),
        ('WLK', [9000, 1, 75, 180]),
    ]

    for workout_type, data in packages:
        training = read_package(workout_type, data)
        main(training)
