⁉️ Welcome! This repository is divided into two main folders.

➡ **GIMAVE/automacoes**: The available automations in this folder were developed to help users complete simple but very manual tasks inside Protheus (ERP developed by Totvs).
I) Baixa Credenciados was created using Selenium to navigate through Protheus, access Accounts Payable and create bordereaus. The script compares Protheus' refund ID with the refund ID generated in another system; if both IDs match, it flags the refund, and once it reaches 100 refunds, it saves the bordereau and continues through the list until it finishes.
II) Fontes Protheus are some sources distributed by an external consultant to help develop solutions inside Protheus (credits to Robson).
III) Liberação TEDs is an automation that goes through a range of money transfers (a solution created by the company I work for, GIMAVE) in a spreadsheet and, once the user gets the 'ok', he/she runs the script and it releases the money transfers to the clients' accounts. The daily transfer volume is around 150–200, so this automation became a huge help for the department.

➡ **GIMAVE/erp**: The ERP was created from scratch by myself to mitigate an urgent necessity from the Purchasing Department: budget management.
I) Compras: First designed module, which contains suppliers, products, classes and budget forms. The system allows the creation of budgets, comparison among them in order to validate which one is more economical, and also provides a simple dashboard showing statistics about the budgets for a determined period.
II) Comercial: Module created to help the Sales Department simulate sales. The user can set the quantity and price of each product so the system can calculate the revenue. If the simulation shows a considerable income, the user can save it and the information is sent to another system, called Zoho, to create the contract.
III) Financeiro: My most recent creation. At the moment, I'm working on dashboards for both Accounts Payable and Accounts Receivable, in order to help our board make the best financial decisions.

• **Languages**: Python, HTML, CSS, JS, MySQL, ADVPL (Protheus)