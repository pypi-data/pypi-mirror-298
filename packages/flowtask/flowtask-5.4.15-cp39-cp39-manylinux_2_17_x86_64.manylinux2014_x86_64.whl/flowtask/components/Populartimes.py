import pandas as pd
from querysource.exceptions import DataNotFound as QSNotFound
from ..exceptions import ComponentError, DataNotFound
from .QSBase import QSBase

class Populartimes(QSBase):
    type = "by_placeid"
    _driver = "populartimes"

    def convert_populartimes(self, popular_times: dict):
        # Map day numbers to day names
        day_mapping = {
            "1": "Monday",
            "2": "Tuesday",
            "3": "Wednesday",
            "4": "Thursday",
            "5": "Friday",
            "6": "Saturday",
            "7": "Sunday"
        }
        # Dictionary to hold the final structured data
        converted_data = {}
        # Iterate through each day and its hours
        for day_number, hours in popular_times.items():
            # Get the day name from the mapping
            day_name = day_mapping.get(day_number, "Unknown")
            converted_data[day_name] = {}

            for hour, data in hours.items():
                # Convert the hour to HH:MM:SS format
                # Ensure leading zeroes for single-digit hours
                time_str = f"{int(hour):02}:00:00"
                # Create the structured dictionary
                converted_data[day_name][time_str] = {
                    "hour": int(hour),
                    "human_hour": data["human_hour"],
                    "traffic": data["traffic"],
                    "traffic_status": data["traffic_status"]
                }
        return converted_data

    async def by_placeid(self):
        result = []
        try:
            additional_data = []
            for _, row in self.data.iterrows():
                self._qs.place_id = row['place_id']
                resultset = await self._qs.by_placeid()
                # Convert array into dictionary
                rts = {}
                if 'popular_times' in resultset:
                    resultset['populartimes'] = self.convert_populartimes(
                        resultset['popular_times']
                    )
                    del resultset['popular_times']
                for component in resultset["address_components"]:
                    key = component["types"][0]
                    value = component["long_name"]
                    rts[key] = value
                resultset["address_components"] = rts
                # Store this row's data for later addition to the DataFrame
                additional_data.append(resultset)
            # Create a DataFrame from the list of dictionaries
            df = pd.DataFrame(additional_data)
            # Concatenate the additional DataFrame with the original DataFrame
            self.data = pd.concat(
                [self.data.reset_index(drop=True), df.reset_index(drop=True)],
                axis=1
            )
            return self.data
        except QSNotFound as err:
            raise DataNotFound(f"Populartimes Not Found: {err}") from err
        except Exception as err:
            self._logger.exception(err)
            raise ComponentError(f"Populartimes ERROR: {err!s}") from err
