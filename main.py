import mercado_libre
import notion_interaction


if __name__ == '__main__':
    mercado_libre_list = mercado_libre.scrape_all()
    notion_interaction.write_data(mercado_libre_list)