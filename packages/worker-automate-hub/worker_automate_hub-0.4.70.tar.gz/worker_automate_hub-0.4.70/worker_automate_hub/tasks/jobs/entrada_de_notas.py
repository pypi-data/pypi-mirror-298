import asyncio
import warnings

import pyperclip
import pyautogui
from pywinauto.application import Application
from rich.console import Console

from worker_automate_hub.api.client import get_config_by_name
from worker_automate_hub.utils.logger import logger
from worker_automate_hub.utils.util import (
    find_target_position,
    import_nfe,
    kill_process,
    login_emsys,
    select_model_capa,
    take_screenshot,
    type_text_into_field,
    verify_import_nf,
    verify_nf_incuded,
    rateio_window
)

pyautogui.PAUSE = 0.5
console = Console()



async def entrada_de_notas(task):
    """
    Processo que relazia entrada de notas no ERP EMSys(Linx).

    """
    try:
        #Get config from BOF
        config = await get_config_by_name("login_emsys")
        console.print(task)
       
        #Seta config entrada na var nota para melhor entendimento
        nota = task['configEntrada']

        #Abre um novo emsys
        await kill_process("EMSys")
        app = Application(backend='win32').start("C:\\Rezende\\EMSys3\\EMSys3.exe")
        warnings.filterwarnings("ignore", category=UserWarning, message="32-bit application should be automated using 32-bit Python")
        console.print("\nEMSys iniciando...", style="bold green")
        return_login = await login_emsys(config['conConfiguracao'], app, task)

        if return_login['sucesso'] == True:
            type_text_into_field('Nota Fiscal de Entrada', app['TFrmMenuPrincipal']['Edit'], True, '50')
            pyautogui.press('enter')
            await asyncio.sleep(1)
            pyautogui.press('enter')
            console.print(f"\nPesquisa: 'Nota Fiscal de Entrada' realizada com sucesso", style="bold green")
        else:
            logger.info(f"\nError Message: {return_login["retorno"]}")
            console.print(f"\nError Message: {return_login["retorno"]}", style="bold red")
            return return_login
        
        await asyncio.sleep(10)
        #Procura campo documento
        model  = select_model_capa()
        if model['sucesso'] == True:
            console.log(model['retorno'], style='bold green')
        else:
            return {"sucesso": False, "retorno": f"{model['retorno']}"}

        #Clica em 'Importar-Nfe'
        imported_nfe  = import_nfe()
        if imported_nfe['sucesso'] == True:
            console.log(imported_nfe['retorno'], style='bold green')
        else:
            return {"sucesso": False, "retorno": f"{import_nfe['retorno']}"}

        await asyncio.sleep(10)

        #Seleciona 'Notas de outras empresas'
        pyautogui.click(818, 546)
        #Clica em  'OK' para selecionar
        pyautogui.click(970, 666)
        await asyncio.sleep(3)

        #Tela importa nota de outra empresa
        #Seleciona Empresa externa
        screenshot_path = take_screenshot()
        field = find_target_position(screenshot_path, "de", 30, 0, 15)
        if field == None:
            return {"sucesso": False, "retorno": f"Não foi possivel encontrar o campo 'Empresa'"}
        pyautogui.click(field)
        pyautogui.write(str(int(nota['cnpjFornecedor'][8:12])))
        pyautogui.hotkey('tab')

        #Digita datas de emissão
        field = find_target_position(screenshot_path, "emissão", 0, 40, 15)
        if field == None:
            return {"sucesso": False, "retorno": f"Não foi possivel encontrar o campo 'Data de emissão inicio'"}
        pyautogui.click(field)
        pyautogui.write(nota['dataEmissao'].replace('/', ''))

        field = find_target_position(screenshot_path, "a", 0, 40, 15)
        if field == None:
            return {"sucesso": False, "retorno": f"Não foi possivel encontrar o campo 'Data de emissão fim'"}
        pyautogui.click(field)
        pyautogui.write(nota['dataEmissao'].replace('/', ''))

        #Digita numero da nota
        field_num = find_target_position(screenshot_path, "Núm", 0, 60, 15)
        if field_num == None:
           return {"sucesso": False, "retorno": f"Não foi possivel encontrar o campo 'Núm Nota'"}
        pyautogui.click(field)
        if nota['numeroNota']:
            pyautogui.write(nota['numeroNota'])

        #TODO bater print para comprovar se a tela da pesquisa não vai estar minimizada
        #Clica em pesquisar
        field = find_target_position(screenshot_path, "pesquisar", 0 ,0, 15)
        if field == None:
            return {"sucesso": False, "retorno": f"Não foi possivel encontrar o botão 'Pesquisar'"}
        pyautogui.click(field)

        await asyncio.sleep(120)
        #TODO verificar se encontrou nota
        nota_exists = verify_import_nf()
        if nota_exists == True:
            console.log("Nota encontrada.")
            #Clica na nota
            pyautogui.click(791,483)
            await asyncio.sleep(2)
        else:
            console.log("Nota não encontrada após o delay.", style='bold green')
            return {"sucesso": False, "retorno": f"Nota não encontrada após o delay."}

        #TODO verificar se nao esta minimizado a tela de pesquisa de nota
        

        #Clica em 'Importar'
        field = find_target_position(screenshot_path, "cancelar",0 ,100 , 15)
        if field == None:
            return {"sucesso": False, "retorno": f"Não foi possivel encontrar o botão importar"}
        pyautogui.click(field)
        
        await asyncio.sleep(10)

        #Identifica se ja foi importada
        screenshot_path = take_screenshot()
        field = find_target_position(screenshot_path, "Mensagem", 0, 0, 10)
        if field == None:
            ...
        else:
            console.log("Nota já lançada ou não encontrada.", style='bold green')
            return {"sucesso": False, "retorno": f"Nota já lançada ou não encontrada."}


        #Tela "Infromações para importação da Nota Fiscal Eletrônica"
        screenshot_path = take_screenshot()

        if nota['existeDespesa'] == 'Sim':
            #Digita natureza da operação
            pyautogui.hotkey('tab')
            pyautogui.write("1152")
            pyautogui.hotkey('tab')

            #Digita tipo despesa
            field = find_target_position(screenshot_path, "Despesa", 15, 40, 15)
            if field == None:
                return {"sucesso": False, "retorno": f"Não foi possivel encontrar o campo despesa"}
            pyautogui.click(field)
            pyautogui.write("291")
            pyautogui.hotkey("tab")

            #Marca "Manter Natureza de operação selecionada"
            pyautogui.click(963, 578)
            #Marca "Manter Calculo PIS/COFINS"
            pyautogui.click(705, 667)

        #Clica em OK
        pyautogui.click(1100, 730)
        await asyncio.sleep(90)

        #Tratativa de "itens com ncm divergente" - PASSO 27.1 DA IT
        screenshot_path = take_screenshot()
        console.log("Procurando itens com ncm divergente", style='bold yellow')
        itens = find_target_position(screenshot_path, 'NCM', 0, 0, 10)
        if itens is not None:
            pyautogui.click(1000,568)
            console.log("Clicou em não nos itens com ncm divergente", style='bold yellow')
        else:
            console.log("0 Itens com ncm divergente", style='bold green')

        await asyncio.sleep(10)

        #Itens não localizados
        #Clica em Sim
        screenshot_path = take_screenshot()
        console.log("Verificando tela de Itens Não Localizado", style='bold yellow')
        itens_nloc = find_target_position(screenshot_path, 'associar', 0, 0, 10)
        if itens_nloc:
            pyautogui.click(920, 562)
            await asyncio.sleep(3)
            pyautogui.click(920, 304)
            pyautogui.hotkey("ctrl", "c")
            clipboard = pyperclip.paste()
            if clipboard:
                console.log("Itens não localizados na nota.", style='bold red')
                return {"sucesso": False, 'retorno':f"Itens não localizado: {clipboard}"}
        
        #trativa "Selecionar itens fornecedor" - PASSO 27.3 da it
        multi_ref = True
        while multi_ref:
            screenshot_path = take_screenshot()
            field = find_target_position(screenshot_path, "fornecedor", 0, 0, 5)
            if field:
                pyautogui.click(1075, 624)
                await asyncio.sleep(20)
            else:
                multi_ref = False
        # else:
        #     console.log("Não existe tela 'Selecionar itens fornecedor'", style='bold green')

        #Seleciona pagamento
        screenshot_path = take_screenshot()
        field = find_target_position(screenshot_path, "pagamento", 0, 0, 15)
        if field == None:
            return {"sucesso": False, "retorno": f"Não foi possivel encontrar o campo de seleção de pagamento"}
        pyautogui.click(field)
        await asyncio.sleep(1)
        
        #Seleciona "Espécie de Caixa"
        screenshot_path = take_screenshot()
        field = find_target_position(screenshot_path, "Espécie", 0, 100, 15)
        if field == None:
            return {"sucesso": False, "retorno": f"Não foi possivel encontrar o campo para selecionar espécie de caixa"}
        pyautogui.click(field)
        pyautogui.write("27")
        pyautogui.hotkey("enter")
    
        #Digita "Valor"
        field = find_target_position(screenshot_path, "Documento", 0, 200, 15)
        if field == None:
            return {"sucesso": False, "retorno": f"Não foi possivel encontrar o campo para digitar o valor"}
        pyautogui.doubleClick(field)
        pyautogui.hotkey("ctrl", "a")
        pyautogui.hotkey("del")
        pyautogui.write(nota['valorNota'])

        #Clica para lançar a nota
        pyautogui.click(594, 299)
        await asyncio.sleep(5)
        console.log("Clicou pra lançar nota", style='bold green')

        #Variação Maxima de custo
        pyautogui.click(1234, 633)
        console.log("Clicou 'OK' variacao maxima de custo", style='bold green')

        #Quantidade de tempo alta devido o emsys ser lento
        console.log("Aguardando delay...", style='bold green')
        await asyncio.sleep(30)

        console.log("Verificando se nota foi lançada", style='bold green')
        retorno = verify_nf_incuded()
        if retorno:
            return {"sucesso": True, "retorno": f"Nota Lançada com sucesso!"}
        else:
            console.log("Verficando se necessita realizar o rateio")
        
        if nota['existeDespesa'] == 'Sim':
            console.log("Inicializando o rateio", style='bold green')
            rateio_window(nota)

        #Aviso CFOP
        console.log("Verificando aviso CFOP", style='bold green')
        screenshot_path = take_screenshot()
        field = None
        field = find_target_position(screenshot_path, "mesmo", 0, 0, 8)
        if field == None:
            console.print("Nota com CFOP correto")
        else:
            #Clica em OK
            pyautogui.click(1096, 603)
            #Clica em "Principal"
            field = find_target_position(screenshot_path, "Principal", 0, 0, 8)
            pyautogui.click(field)
            #Selecio no "Principal" a NOP correta
            field = find_target_position(screenshot_path, "Inscrição", 20, 0, 8)
            pyautogui.click(field)
            pyautogui.write("1152")
            #Clica para lançar a nota
            pyautogui.click(594, 299)

            #Clica novamente em ok na variação de custo      
            field = find_target_position(screenshot_path, "ultrapassam", 0, 0, 8)
            if field == None:
                console.print("Nota sem itens com variação de custo")
            else:
                pyautogui.click(1234, 633)

        #Clica para lançar a nota
        pyautogui.click(594, 299)
        await asyncio.sleep(5)

        #Verifica se a info 'Nota fiscal incluida' está na tela   
        retorno = verify_nf_incuded()
        if retorno:
            return {"sucesso": True, "retorno": f"Nota Lançada com sucesso!"}
        else:
            return {"sucesso": False, "retorno": f"Erro ao lançar nota"}

    except Exception as ex:
        observacao = f"Erro Processo Entrada de Notas: {str(ex)}"
        logger.error(observacao)
        console.print(observacao, style="bold red")
        return {"sucesso": False, "retorno": observacao}

