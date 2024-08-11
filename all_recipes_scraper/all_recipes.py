import requests


class AllRecipes:
    def __init__(self):
        self.base_url = "https://www.allrecipes.com/recipes"
        self.url = (
            self.base_url
            + "/17057/everyday-cooking/more-meal-ideas/5-ingredients/main-dishes/"
        )
        self.get_html()

    def get_html(self, from_disk=True):
        if from_disk:
            try:
                with open("dump.txt", "r") as f:
                    self.html_text = f.read()
            except FileNotFoundError as e:
                print(e)
                self.get_html(from_disk=False)
        else:
            headers = {
                "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.0.0 Safari/537.36",
            }
            response = requests.get(url=self.url, headers=headers)
            self.html_text = response.text
            with open("dump.txt", "w") as f:
                f.write(self.html_text)
