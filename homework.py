class InfoMessage:
    """
    Информационное сообщение о тренировке.
    Получает данные из класса тренировка и создает
    сообщение - строку для вывода на экран.
    Методы класса:
    get_message
    """

    def __init__(
            self,
            training_type: str,
            duration: int,
            distance: float,
            speed: float,
            calories: float) -> None:
        self.speed: float = speed
        self.duration: int = duration
        self.calories: float = calories
        self.distance: float = distance
        self.training_type: str = training_type

    def get_message(self):
        """
        Преобразовать данные в строку и округлить
        числовые значения до 3 знаком после запятой.
        """
        return (f'Тип тренировки: {self.training_type}; '
                f'Длительность: {self.duration:.3f} ч.; '
                f'Дистанция: {self.distance:.3f} км; '
                f'Ср. скорость: {self.speed:.3f} км/ч; '
                f'Потрачено ккал: {self.calories:.3f}.')


class Training:
    """
    Базовый класс тренировки.
    Передает медод для вывода сообщения на экран другим
    наследующим классам.
    Создает методы вычисления пройденного расстояния и средней
    скорости для наследующих классов, кроме класса swim.
    Описывает сруктуру наследующик класов.
    Memoды класса: [get_distance, get_mean_speed, get_spent_calories
    show_training_info]
   """
    LEN_STEP: float = 0.65
    M_IN_KM: int = 1000
    MIN_IN_H: int = 60

    def __init__(
            self,
            action: int,
            duration: int,
            weight: float) -> None:
        self.duration: int = duration
        self. weight: float = weight
        self.action: int = action

    def get_distance(self) -> float:
        """
        Получить дистанцию (в километрах),
        которую преодолел пользователь за время тренировки.
        """
        traveled_in_total = self.action * self.LEN_STEP / self.M_IN_KM
        return traveled_in_total

    def get_mean_speed(self) -> float:
        """
        Получить среднюю скорость движения
        во время тренировки в км/ч.
        """
        average_speed = self.get_distance() / self.duration
        return average_speed

    def get_spent_calories(self):
        """
        Получить количество затраченных калорий
        израсходованных за время тренировки.
        """
        pass

    def show_training_info(self) -> InfoMessage:
        """
        Вернуть сообщение о выполненной тренировке.
        возвращает объект класса сообщения.
        """
        workout_session_mode = self.__class__.__name__
        conducted_training_summary_report: InfoMessage = InfoMessage(
            workout_session_mode,
            self.duration,
            self.get_distance(),
            self.get_mean_speed(),
            self.get_spent_calories())
        return conducted_training_summary_report


class Running(Training):
    """
    Класс создает оригинальный метод для рассчета калорий и вывода
    инофрмации о тренировке бег с помощью метода show_training_info
    базового класса.
    Memoды класса: [get_distance, get_mean_speed, get_spent_calories
    show_training_info]
   """
    CALORIES_MEAN_SPEED_SHIFT: float = 1.79
    CALORIES_MEAN_SPEED_MULTIPLIER: int = 18

    def __init__(
            self,
            action: int,
            duration: int,
            weight: float) -> None:
        super().__init__(action, duration, weight)
        self. CALORIES_MEAN_SPEED_MULTIPLIER: int = 18
        self.CALORIES_MEAN_SPEED_SHIFT: float = 1.79

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        s = self.CALORIES_MEAN_SPEED_MULTIPLIER * self.get_mean_speed()
        avg_s_adj = s + self.CALORIES_MEAN_SPEED_SHIFT
        weight_index = avg_s_adj * self.weight
        weight_index_per_minute = weight_index / self.M_IN_KM
        kall = weight_index_per_minute * self.duration * self.MIN_IN_H
        return kall


class SportsWalking(Training):
    """
    Класс создает оригинальный метод для рассчета калорий и вывода
    инофрмации о тренировке спортивная ходьба с помощью
    метода show_training_info базового класса.
    Memoды класса: [get_distance, get_mean_speed, get_spent_calories
    show_training_info]
   """
    CM_IN_M: int = 100
    KMH_IN_MSEC: float = 0.278
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
        kall = weight_index_addition * self.duration * self.MIN_IN_H
        return kall


class Swimming(Training):
    """
    Класс создает оригинальный метод для рассчета калорий
    и вывода инофрмации о тренировке плавание с помощью
    метода show_training_info базового класса.
    Переопределяет базовый метод получения средней скорости.
    Memoды класса: [get_distance, get_mean_speed, get_spent_calories
    show_training_info]
   """
    CALORIES_MEAN_SPEED_SHIFT: float = 1.1
    CALORIES_WEIGHT_MULTIPLIER: int = 2
    LEN_STEP: float = 1.38

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
        kall = speed * calories_amount_by_speed_unit
        return kall


def read_package(
        workout_type: str,
        data: list) -> Training:
    """
    Прочитать данные полученные от датчиков.
    Определяет тип тренировки и создает instance класса тренировки.
    """
    select_class_variant_dicktionary = {
        'SWM': Swimming,
        'RUN': Running,
        'WLK': SportsWalking
    }
    selected_class = select_class_variant_dicktionary[workout_type]
    training = selected_class(*data)
    return training


def main(training: Training) -> None:
    """
    Главная функция.
    Вызывает метод создания класса тренировки.
    Выводит результат вычислений в консоль фитнес трекера.
    """
    info = training.show_training_info()
    readout = info.get_message()
    print(readout)


if __name__ == '__main__':
    packages: list[tuple[str, list]] = [
        ('SWM', [720, 1, 80, 25, 40]),
        ('RUN', [15000, 1, 75]),
        ('WLK', [9000, 1, 75, 180]),
    ]

    for workout_type, data in packages:
        package = read_package(workout_type, data)
        main(package)
