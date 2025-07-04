import requests
from bs4 import BeautifulSoup


class AnimeHub:
    def __init__(self, headers:dict=None, host:str=None) -> None:
        self.headers = headers if headers else {
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:139.0) Gecko/20100101 Firefox/139.0',
            'Accept': 'application/json',
            'Accept-Language': 'uk-UA,uk;q=0.8,en-US;q=0.5,en;q=0.3',
            'lang': 'ua',
            'Origin': 'https://animehub.land',
            'Connection': 'keep-alive',
            'Referer': 'https://animehub.land/',
            'Sec-Fetch-Dest': 'empty',
            'Sec-Fetch-Mode': 'cors',
            'Sec-Fetch-Site': 'same-site',
        }

        self.host = host if host else 'https://api.animehub.land'


    def get_anime_id_by_slug(self, slug:str) -> str:
        url = f'https://api.animehub.land/api/v1/cinema/anime/{slug}/uuid'
        response = requests.get(url, headers=self.headers)
        if response.status_code == 200:
            data = response.json()
            return data.get("id")
        else:
            print(response.status_code)
            return None

    def get_anime_list(self):
        return


    def get_anime_by_id(self, id:str) -> dict:
        url = f'https://api.animehub.land/api/v1/cinema/anime/{id}'
        response = requests.get(url, headers=self.headers)
        if response.status_code == 200:
            return response.json()
        else:
            print(response.status_code)
            return None


    def get_anime_by_url(self, url:str) -> dict:
        response = requests.get(url, headers=self.headers)
        if response.status_code == 200:
            html = response.text
            soup = BeautifulSoup(html, 'html.parser')
            og_image = soup.find("meta", {"name": "twitter:image"})
            if og_image:
                og_image_url = og_image["content"]
                anime_id = og_image_url.split('/')[-1].split('.')[0]
                return self.get_anime_by_id(anime_id)
            else:
                return None
        else:
            return response.status_code

    def get_episodes_by_id(self, id) -> dict:
        data = self.get_anime_by_id(id)
        video_data = data.get('teams', [])
        return {"teams": video_data}


    def gen_playlist_by_id(self, id):
        studios = []
        data = self.get_episodes_by_id(id)
        for item in data.get("teams", []):
            team = item.get("team", {})
            episodes = item.get("dubbingEpisodes", [])

            studio = {
                "name": team.get("name"),
                "videos": [
                    {
                        "episode": str(ep.get("episodeNumber")),
                        "id": ep.get("id"),
                        "url": f"{self.host}/storage/videos/chucks_for_streaming/{ep.get('id')}/master_playlist.m3u8",
                    }
                    for ep in episodes
                ]
            }

            studios.append(studio)

        return {"studios": studios}
    
    
    def formated_anime_data_by_id(self, id:str) -> dict:
        data = self.get_anime_by_id(id)
        return {
            "title": data.get("nameUa"),
            "title_en": data.get("nameEn"),
            "release_date": data.get("createdAt"),
            "year": data.get("year"),
            "studios": ", ".join([team.get("team", {}).get("name") for team in data.get("teams", [])]),
            "episode": data.get("dubbedEpisodes"),
            "link": f"{self.host}/anime/{data.get('slug')}",
        }
anime = AnimeHub()

#data = anime.get_anime_by_id("99db7135-dc53-4f6b-8ff4-9acf42a2e6a1")
#data = anime.get_anime_by_url("https://animehub.land/anime/monolog-travnici-2")
#data = anime.get_episodes_by_id("7bda84c3-61e1-4436-a58b-1972a94c77c0")
#data = anime.gen_playlist_by_id("7bda84c3-61e1-4436-a58b-1972a94c77c0")
#data = anime.formated_anime_data_by_id("7bda84c3-61e1-4436-a58b-1972a94c77c0")
#data_id = anime.get_anime_id_by_slug("monolog-travnici-2")
#data = anime.gen_playlist_by_id(data_id)
#print(data)