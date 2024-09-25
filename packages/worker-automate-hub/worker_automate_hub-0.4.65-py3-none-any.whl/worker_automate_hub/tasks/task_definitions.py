from worker_automate_hub.tasks.jobs.conexao_rdp import conexao_rdp
from worker_automate_hub.tasks.jobs.descartes import descartes
from worker_automate_hub.tasks.jobs.ecac_estadual_main import ecac_estadual_main
from worker_automate_hub.tasks.jobs.ecac_federal import ecac_federal
from worker_automate_hub.tasks.jobs.entrada_de_notas import entrada_de_notas
from worker_automate_hub.tasks.jobs.fazer_pudim import fazer_pudim
from worker_automate_hub.tasks.jobs.login_emsys import login_emsys
from worker_automate_hub.tasks.jobs.playground import playground
from worker_automate_hub.tasks.jobs.transferencias import transferencias

task_definitions = {
    "5b295021-8df7-40a1-a45e-fe7109ae3902": fazer_pudim,
    "a0788650-de48-454f-acbf-3537ead2d8ed": login_emsys,
    "abcfa1ba-d580-465a-aefb-c15ac4514407": descartes,
    "2c8ee738-7447-4517-aee7-ce2c9d25cea9": transferencias,
    "855f9e0f-e972-4f52-bc1a-60d1fc244e79": conexao_rdp,
    "bf763394-918b-47be-bb36-7cddc81a8174": entrada_de_notas,
    "3907c8d4-d05b-4d92-b19a-2c4e934f1d78": ecac_estadual_main,
    "81d2d6e6-e9eb-414d-a939-d220476d2bab": ecac_federal,
    "a4154a69-a223-48c2-8ff6-535cd29ff2d4": playground,
}


async def is_uuid_in_tasks(uuid_to_check):
    """
    Verifica se um UUID está presente nas definições de tarefas.

    :param uuid_to_check: O UUID a ser verificado.
    :return: True se o UUID estiver presente, False caso contrário.
    """
    return uuid_to_check in task_definitions.keys()
