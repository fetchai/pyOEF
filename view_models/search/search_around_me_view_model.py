from typing import Optional

from starlette.requests import Request

from view_models.shared.viewmodel import ViewModelBase


class SearchAroundMeViewModel(ViewModelBase):
    def __init__(self, request: Request):
        super().__init__(request)

        self.latitude: Optional[float] = None
        self.longitude: Optional[float] = None
        self.radius: Optional[float] = None

    async def load(self):
        request_data = await self.request.json()

        if not all(key in ["latitude", "longitude", "radius"] for key in request_data.keys()):
            self.error = (
                f"You need to provide the following parameters: ['latitude', 'longitude', 'radius'] "
            )
            return

        self.latitude = float(request_data.get("latitude"))
        self.longitude = float(request_data.get("longitude"))
        self.radius = float(request_data.get('radius'))

