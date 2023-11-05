import datetime

class TransformDataPipeline:
    def process_item(self, item, spider):
        fecha_original = datetime.datetime.strptime(item["fecha"], "%d-%m-%Y")
        fecha_transformada = fecha_original.strftime("%Y-%m-%d")

        transformed_product = {
            "fecha": fecha_transformada,
            "nombre": item["nombre"],
            "GSI": item["GSI"],
            "historicos": {},
        }

        for vendedor, precio in zip(item["vendedores"], item["precios"]):
            if vendedor not in transformed_product["historicos"]:
                transformed_product["historicos"][vendedor] = []

            transformed_product["historicos"][vendedor].append(
                {
                    "fecha": fecha_transformada,
                    "precio": precio,
                }
            )

        return transformed_product