class Benefits:
    Name = "Выгоды"
    Initial = "Исходные параметры"
    Inner = "Продажа на внутреннем рынке"
    Outer = "Продажа на экспорт"


class OPEX:
    Name = "Затраты"
    ProdWells = "обслуживание добывающих скважин"
    InjWells = "обслуживание нагнетательных скважин"
    OilPreparation = "подготовка нефти"
    CollectionOil = "сбор и транспорт нефти"
    WaterInjection = "закачка воды"
    MechanizedOil = "Механизированное извлечение нефти"
    MajorOverhaul = "Капитальный ремонт"
    WFRACK = "ГРП"
    ReservoirIsolation = "изоляция пласта"
    Others = "прочие"


class CAPEX:
    Name = "Капитал"
    DrillProdWell = "1. БУРЕНИЕ ДОБЫВАЮЩИХ СКВАЖИН"
    DrillInjeWell = "2. БУРЕНИЕ НАГНЕТАТЕЛЬНЫХ СКВАЖИН"
    WellMechanization = "3. МЕХАНИЗАЦИЯ СКВАЖИН"
    OilTransportation = "4. СБОР И ТРАНСПОРТ НЕФТИ"
    BoosterPumping = "5. ДНС с УПСВ"
    PowerSupply = "6. ЭЛЕКТРОСНАБЖЕНИЕ И СВЯЗЬ"
    WaterSupply = "7. ПРОМВОДОСНАБЖЕНИЕ"
    Roads = "8. ПРОМЫСЛОВЫЕ ДОРОГИ"
    ReservoirPressureSupport = "9.ППД"
    Ecology = "10. ЗАТРАТЫ НА ЭКОЛОГИЮ"
    Others = "11. ПРОЧИЕ"


class Tax:
    Name = "Налоги"
    Property = "Налог на имущество"
    Income = "Налог на прибыль"
    LandPayment = "Плата за землю"
    MineralExtraction = "НДПИ"
    InsurancePremiums = "Страховые взносы"
    InsuranceAccident = "Страхование от несчастных случаев"


class Credits:
    Name = "Долг"
    Method = "Метод"
    LoanAmount = "ПОСТУПЛЕНИЕ".upper()
    IssueTime = "Момент выдачи".upper()
    GracePeriod = "Льготный период".upper()
    InterestRate = "Процентная ставка".upper()
    LoanTime = "Длительность займа".upper()
    InterestCapital = "Капитализация процентов".upper()
    Years = "ГОД"


class Currency:
    Name = "Валюта"
    USD = "USD"


class PivotTable:
    Name = "Фин"
    NPV = "NPV"
