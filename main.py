from all_recipes_scraper.all_recipes import AllRecipes


def scrape_page():
    all_recipes = AllRecipes()
    all_recipes.get_html(from_disk=True)
    all_recipes.parse_html()
    all_recipes.save_recipe_info()


if __name__ == "__main__":
    scrape_page()
