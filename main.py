from dataclasses import dataclass


@dataclass
class InfoMessage:
    """
    Информационное сообщение о тренировке.
    Получает данные из show_training_info.
    Создает строку сообщение.
    Методы класса: get_message
    """
    training_type: str
    duration: int
    distance: float
    speed: float
    calories: float

    MESSAGE = ('Тип тренировки: {training_type}; '
               'Длительность: {duration} ч.; '
               'Дистанция: {distance} км; '
               'Ср. скорость: {speed} км/ч; '
               'Потрачено ккал: {calories}.')

    def __setattr__(self, key, value):
        """Все числовые значения округлять до 3 знаком после запятой."""
        value = (f'{value:.3f}'
                 if type(value) in (int, float)
                 else value)
        return object.__setattr__(self, key, value)

    def get_message(self):
        """Вернуть строку с полученными данными."""
        return self.MESSAGE.format(**self.__dict__)


class Training:
    """
    Базовый класс тренировки.
    Передает метод для вывода сообщения на экран другим
    наследующим классам.
    Создает методы вычисления пройденного расстояния и средней
    скорости для наследующих классов, кроме класса swim.
    Описывает структуру наследующих классов.
    Методы класса:
    get_distance | get_mean_speed | get_spent_calories | show_training_info
   """
    MIN_IN_H: float = 60.0  # minutes in hour
    M_IN_KM: float = 1000.0  # meters in kilometer
    LEN_STEP: float = 0.65  # meters in human step

    def __init__(
            self,
            action: int,
            duration: int,
            weight: float) -> None:
        self.duration: int = duration
        self.weight: float = weight
        self.action: int = action

    def get_distance(self) -> float:
        """Получить дистанцию (в километрах) за время тренировки."""
        traveled_in_total = self.action * self.LEN_STEP / self.M_IN_KM
        return traveled_in_total

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения в км/ч."""
        average_speed = self.get_distance() / self.duration
        return average_speed

    def get_spent_calories(self):
        """Получить количество затраченных калорий за время тренировки."""
        if __name__ == '__main__':
            raise NotImplementedError
        pass

    def show_training_info(self) -> InfoMessage:
        """
        Вернуть сообщение о выполненной тренировке.
        Возвращает объект класса сообщения.
        """
        workout_session_mode = type(self).__name__
        summary_training_report: InfoMessage = InfoMessage(
            workout_session_mode,
            self.duration,
            self.get_distance(),
            self.get_mean_speed(),
            self.get_spent_calories())
        return summary_training_report


class Running(Training):
    """
    Класс создает оригинальный метод для расчёта калорий и вывода
    информации о тренировке бег с помощью метода show_training_info
    базового класса.
    Методы класса:
    get_distance | get_mean_speed | get_spent_calories | show_training_info
   """
    CALORIES_MEAN_SPEED_SHIFT: float = 1.79
    CALORIES_MEAN_SPEED_MULTIPLIER: float = 18.0

    def __init__(
            self,
            action: int,
            duration: int,
            weight: float) -> None:
        super().__init__(action, duration, weight)

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        s = self.CALORIES_MEAN_SPEED_MULTIPLIER * self.get_mean_speed()
        avg_s_adj = s + self.CALORIES_MEAN_SPEED_SHIFT
        weight_index = avg_s_adj * self.weight
        weight_index_per_minute = weight_index / self.M_IN_KM
        cal = weight_index_per_minute * self.duration * self.MIN_IN_H
        return cal


class SportsWalking(Training):
    """
    Класс создает оригинальный метод для расчета калорий и вывода
    информации о тренировке спортивная ходьба с помощью
    метода show_training_info базового класса.
    Методы класса:
    get_distance | get_mean_speed | get_spent_calories | show_training_info
   """
    CM_IN_M: float = 100.0  # sentiments in meter
    KMH_IN_MSEC: float = 0.278  # kph to mps reformer
    CALORIES_WEIGHT_MULTIPLIER: float = 0.035
    CALORIES_SPEED_HEIGHT_MULTIPLIER: float = 0.029

    def __init__(
            self,
            action: int,
            duration: int,
            weight: float,
            height: int) -> None:
        super().__init__(action, duration, weight)
        self.height: int = height

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        height_in_m = self.height / self.CM_IN_M
        average_speed_mps = self.get_mean_speed() * self.KMH_IN_MSEC
        weight_index = self.CALORIES_WEIGHT_MULTIPLIER * self.weight
        cal_wt = self.CALORIES_SPEED_HEIGHT_MULTIPLIER * self.weight
        total_cals = (average_speed_mps ** 2 / height_in_m) * cal_wt
        weight_index_addition = weight_index + total_cals
        cal = weight_index_addition * self.duration * self.MIN_IN_H
        return cal


class Swimming(Training):
    """
    Класс создает оригинальный метод для расчета калорий
    и вывода информации о тренировке плавание с помощью
    метода show_training_info базового класса.
    Переопределяет базовый метод получения средней скорости.
    Методы класса:
    get_distance | get_mean_speed | get_spent_calories | show_training_info
   """
    CALORIES_MEAN_SPEED_SHIFT: float = 1.1
    CALORIES_WEIGHT_MULTIPLIER: float = 2.0
    LEN_STEP: float = 1.38  # meters, swimming stroke length

    def __init__(
            self,
            action: int,
            duration: int,
            weight: int,
            length_pool: int,
            count_pool: int) -> None:
        super().__init__(action, duration, weight)
        self.length_pool: int = length_pool
        self.count_pool: int = count_pool

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения."""
        accumulated_on_lap = self.length_pool * self.count_pool
        accumulated_on_lap_km = accumulated_on_lap / self.M_IN_KM
        average_speed = accumulated_on_lap_km / self.duration
        return average_speed

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        speed = self.get_mean_speed() + self.CALORIES_MEAN_SPEED_SHIFT
        add_multiplier = self.CALORIES_WEIGHT_MULTIPLIER * self.weight
        calories_amount_by_speed_unit = add_multiplier * self.duration
        cal = speed * calories_amount_by_speed_unit
        return cal


def verify_data(
        workout_type: str,
        training_types: list,
        workout_data: list) -> None:
    if workout_type not in training_types:
        raise TypeError(f'read package error: '
                        f'unknown type of training: {workout_type}'
                        f'acceptable types: {training_types}')
    is_not_numbers = list(filter(lambda num:
                                 type(num) not in (int, float),
                                 workout_data)
                          )
    if len(is_not_numbers) > 0:
        raise ValueError('read package error: '
                         'incorrect data type, '
                         'all values should be a number')

    data_values_amount = {'SWM': 5, 'RUN': 3, 'WLK': 4}[workout_type]
    if data_values_amount != len(workout_data):
        raise ValueError('read package error: '
                         'incorrect number of values received'
                         f'training type: {workout_type} '
                         f'should accept {data_values_amount} values')


def read_package(
        workout_type: str,
        workout_data: list) -> Training:
    """Определяет тип тренировки и создает класс нужного типа"""
    training_class = {
        'SWM': Swimming,
        'RUN': Running,
        'WLK': SportsWalking
    }
    training_types = [*training_class]
    verify_data(workout_type, training_types, workout_data)

    selected_class = training_class[workout_type]
    training = selected_class(*workout_data)
    return training


def main(training: Training) -> None:
    """Вызывает метод show_training_info, выводит результат в консоль."""
    info = training.show_training_info()
    readout = info.get_message()
    print(readout)


if __name__ == '__main__':
    packages: list = [
        ('SWM', [720, 1, 80, 25, 40]),
        ('RUN', [15000, 1, 75]),
        ('WLK', [9000, 1, 75, 180]),
    ]

    for str_workout_type, data in packages:
        package = read_package(str_workout_type, data)
        main(package)
