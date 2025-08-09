import json
import ast
from util.common import get_template_params_for_upsert

class TemplateAccessor:
    def __init__(self, connection) -> None:
        self.connection = connection
        pass

    def save_template(self, payload):
        query_params = get_template_params_for_upsert(payload)
        cursor = self.connection.cursor()
        cursor.execute("""
        INSERT INTO templates(id, widget, device, data, created_date, modified_date)
        VALUES(:id, :widget, :device, :layout, datetime('now'), datetime('now'))
        ON CONFLICT(widget, device) DO UPDATE SET data= :layout, modified_date=datetime('now');
        """, query_params
        )
        self.connection.commit()
    
    def get_all_templates(self):
        all_templates = self.connection.execute("""
        SELECT * from templates
        """).fetchall()
        formatted_templates = {}
        for template in all_templates:
            layout = template[1]
            widget = template[2]
            device = template[3]
            if widget not in formatted_templates:
                formatted_templates[widget] = {}
            formatted_templates[widget][device] = ast.literal_eval(layout)
        return formatted_templates
