from stadium import Stadium

class OlympicVelodrome(Stadium):
    def __init__(self):
        super().__init__(
            length=250,
            radius=24.37,
            width=8,
            straight_banking=12,
            curve_banking=45,
        )

class OutdoorAthleticsTrack(Stadium):
    def __init__(self):
        super().__init__(
            length=400,
            radius=36.5,
            width=8,
            straight_banking=0,
            curve_banking=0,
        ) 

class IndoorAthleticsTrack(Stadium):
    def __init__(self):
        super().__init__(
            length=200,
            radius=18.5,
            width=8,
            straight_banking=0,
            curve_banking=10,
        )
