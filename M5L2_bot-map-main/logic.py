import sqlite3
import matplotlib.pyplot as plt
import cartopy.crs as ccrs
import cartopy.feature as cfeature
from config import DATABASE

class MapBot:
    def __init__(self):
        self.db = DATABASE
    
    def find_city(self, city_name):
        """Найти город в базе данных"""
        conn = sqlite3.connect(self.db)
        cursor = conn.cursor()
        
        # Ищем город (регистронезависимо)
        cursor.execute("""
            SELECT city, lat, lng FROM cities 
            WHERE LOWER(city) = LOWER(?)
        """, (city_name,))
        
        result = cursor.fetchone()
        conn.close()
        
        return result  # (название, широта, долгота)
    
    def draw_city_on_world_map(self, city_name, lat, lon):
        """Нарисовать город на карте мира"""
        # Карта мира
        fig = plt.figure(figsize=(12, 6))
        ax = plt.axes(projection=ccrs.PlateCarree())
        ax.set_global()
        
        # Базовая карта
        ax.add_feature(cfeature.LAND, facecolor='lightgray')
        ax.add_feature(cfeature.OCEAN, facecolor='lightblue')
        ax.add_feature(cfeature.COASTLINE, linewidth=0.5)
        
        # Город
        ax.plot(lon, lat, 'ro', markersize=10, 
                transform=ccrs.PlateCarree())
        ax.text(lon + 3, lat + 2, city_name,
               transform=ccrs.PlateCarree(),
               fontsize=12, fontweight='bold')
        
        # Сохраняем
        filename = f"{city_name.replace(' ', '_')}.png"
        plt.title(f'Город: {city_name}', fontsize=14)
        plt.savefig(filename, dpi=120, bbox_inches='tight')
        plt.close()
        
        return filename