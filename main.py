from all_recipes_scraper.all_recipes import AllRecipes


def scrape_page():
    all_recipes = AllRecipes()
    all_recipes.get_html(from_disk=True)


if __name__ == "__main__":
    scrape_page()