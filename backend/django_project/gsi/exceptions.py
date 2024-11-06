# class InvalidGsiData(Exception):
#     """Raised when structure of GSI data dont match expected"""
#     def __init__(self):
#         self.message = 'Invalid GSI data.'
#         super().__init__(self.message)


class UserGsiTokenError(Exception):
    """Raised when dont found user with recieved GSI token"""
    def __init__(self, gsi_token: str):
        self.message = 'Recieved GSI Data contains token of unknown user. '
        self.message += f'GSI token: {gsi_token}'
        super().__init__(self.message)
