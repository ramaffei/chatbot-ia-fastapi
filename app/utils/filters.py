from difflib import SequenceMatcher
from typing import Any


def filter_by_key(data: list, key: str, value: Any, exact: bool = False) -> list:
    """
    Se filtran los datos de acuerdo al codigo de instrumento

    Args:
        movimientos (list): data
        filtro (str): cadena a buscar

    Returns:
        list: data filtrada
    """

    if type(value) is int or type(value) is bool or exact:
        return list(filter(lambda d: str(value).lower() == str(d[key]).lower(), data))
    elif type(value) is str:
        return list(filter(lambda d: value.lower() in str(d[key]).lower(), data))
    else:
        raise ValueError("Param value is not type int, str or bool")


def filtrar_lista(
    lista: list[dict], filtro: int | bool | str, keys: list[str], exacto: bool = True
) -> list[dict]:
    if not isinstance(filtro, (int, bool, str)):
        raise ValueError("El parámetro 'value' debe ser de tipo int, str o bool.")

    resultado = []
    ya_filtrados = set()

    filtro_str = str(filtro).lower()

    for item in lista:
        item_id = id(item)
        if item_id in ya_filtrados:
            continue

        for key in keys:
            valor = item.get(key)
            if valor is None:
                break

            valor_str = str(valor).lower()

            if isinstance(valor, (int, bool)) or exacto:
                if valor_str == filtro_str:
                    resultado.append(item)
                    ya_filtrados.add(item_id)
                    break
            else:
                if filtro_str in valor_str:
                    resultado.append(item)
                    ya_filtrados.add(item_id)
                    break
    return resultado


def buscar_dicc(it: list[dict], clave: str, valor: Any) -> dict:
    for dicc in it:
        if clave in dicc and dicc[clave] == valor:
            return dicc
    return {}


def calcular_similitud(
    dic: dict, valor_busqueda: str, keys_search: list | None = None
) -> float:
    if keys_search is None:
        valores_concatenados = " ".join(str(v).lower() for v in dic.values())
    else:
        valores_concatenados = " ".join(
            str(v).lower() for k, v in dic.items() if k in keys_search
        )
    return SequenceMatcher(None, valor_busqueda.lower(), valores_concatenados).ratio()


def filtrar_por_busqueda(
    data: dict[str, str], filter_busqueda: str, filters_keys: list[str]
) -> bool:
    return any(
        filter_busqueda is None
        or filter_busqueda.lower() in (data.get(key, "")).lower()
        for key in filters_keys
    )


def filtrar_por_atributos(data: dict[str, Any], filters: dict[str, str]) -> bool:
    for key, filtro in filters.items():
        atributo_valor = data.get(key)
        if atributo_valor is None or filtro is None:
            continue

        filtro_str = str(filtro).lower()
        atributo_valor_str = str(atributo_valor).lower()

        if isinstance(atributo_valor, (int, bool)):
            if atributo_valor_str != filtro_str:
                return False
        elif isinstance(atributo_valor, str):
            if filtro_str not in atributo_valor_str:
                return False
        else:
            raise ValueError(
                f"El valor ({filtro}) del filtro {key} debe ser de tipo int, str o bool."
            )
    return True
