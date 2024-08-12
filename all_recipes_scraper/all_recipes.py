import csv
from bs4 import BeautifulSoup
import requests


class AllRecipes:
    def __init__(self):
        self.base_url = "https://www.allrecipes.com/recipes"
        self.url = (
            self.base_url
            + "/17057/everyday-cooking/more-meal-ideas/5-ingredients/main-dishes/"
        )

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

    def parse_html(self):
        self.soup = BeautifulSoup(self.html_text, "html.parser")
        self.get_recipes_list()
        self.extract_recipe_info()

    def get_recipes_list(self):
        recipes_list_class = "tax-sc__recirc-list"
        recipes_list = self.soup.find_all(class_=recipes_list_class)
        recipes = [i.find_all(class_="mntl-card-list-items") for i in recipes_list]
        self.recipes = [recipe for recipes_list in recipes for recipe in recipes_list]

    def extract_recipe_info(self):
        def _get_star_rating(i):
            full_stars = i.find_all(class_="icon-star")
            half_stars = i.find_all(class_="icon-star-half")
            star_rating = len(full_stars) + (len(half_stars) / 2)
            return star_rating

        def _get_num_ratings(i):
            num_ratings_class = "mm-recipes-card-meta__rating-count-number"
            num_ratings_string = i.find(class_=num_ratings_class).contents[0].strip()
            num_ratings_int = int(num_ratings_string.replace(",", ""))
            return num_ratings_int

        def _get_content_tags(i):
            tags = i.find(class_="card__content").get("data-tag")
            return tags

        recipe_urls = [recipe.get("href") for recipe in self.recipes]
        titles = [
            recipe.find(class_="card__title-text").getText() for recipe in self.recipes
        ]
        ratings = [_get_star_rating(recipe) for recipe in self.recipes]
        num_ratings = [_get_num_ratings(recipe) for recipe in self.recipes]
        tags = [_get_content_tags(recipe) for recipe in self.recipes]
        self.recipes_info = [
            {
                "title": title,
                "url": url,
                "rating": rating,
                "num_ratings": num_rating,
                "tag": tag,
            }
            for title, url, rating, num_rating, tag in zip(
                titles, recipe_urls, ratings, num_ratings, tags
            )
        ]

    def save_recipe_info(self):
        header = ["title", "url", "rating", "num_ratings", "tag"]
        with open("recipes.csv", "w", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=header)
            writer.writeheader()
            for row in self.recipes_info:
                writer.writerow(row)
