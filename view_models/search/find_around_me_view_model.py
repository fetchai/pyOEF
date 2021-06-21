from typing import Optional

from starlette.requests import Request

from view_models.shared.viewmodel import ViewModelBase


class FindAroundMeViewModel(ViewModelBase):
    def __init__(self, request: Request):
        super().__init__(request)

        self.latitude: Optional[float] = None
        self.longitude: Optional[float] = None
        self.radius: Optional[float] = None
        self.genus: Optional[str] = None
        self.classification: Optional[str] = None

    async def load(self):
        request_data = await self.request.json()

        if not all(key in request_data.keys() for key in ["latitude", "longitude", "radius"]):
            self.error = (
                f"You need to provide the following parameters: ['latitude', 'longitude', 'radius'] "
            )
            return

        self.latitude = float(request_data.get("latitude"))
        self.longitude = float(request_data.get("longitude"))
        self.radius = float(request_data.get('radius'))
        if "genus" in request_data.keys() and request_data.get('genus') != '':
            self.genus = request_data.get('genus')
        if "classification" in request_data.keys() and request_data.get('classification') != '':
            self.classification = request_data.get('classification')

