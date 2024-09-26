import tests_settings  # noqa: F401
from fastmindapi.modules import FunctionModule

package_list = [
    "/Users/wumengsong/Code/PJLab/ChemAgent/chem_lib"
]

funcmodule = FunctionModule(package_list)

print(funcmodule.get_all_tool_names_list())
print(funcmodule.get_tool_information_text_list(['chem_lib/get_element_properties', 'chem_lib/calculate_element_frequencies_in_compound']))

print(funcmodule.exec_tool_calling("chem_lib/get_element_properties(element='Au')"))
print(funcmodule.tool_pool_dict["chem_lib"].call_tool("get_element_properties",["Au"]))