⁉️ **Welcome! This repository is divided in two main folders.**


➡ **GIMAVE/automacoes**: The avaiable automatizations in this folder were developed to help users to complete simple, but very manual tasks inside Protheus (ERP developed by Totvs). I) 'Baixa Credenciados' was created utilizing Selenium to navigate through Protheus, access 'Accounts Payable' and create bordereaus. The script compares Protheus' refund ID with refund's ID generated in another system, if both IDs match it'll flag the refund and when it reaches 100 refunds, it saves the borderau and keeps going through the list until it ends. II) 'Fontes Protheus' are some fonts distributed by an external consultant to help develop some solutions inside Protheus, credits to Robson. III) 'Liberação TEDs' is an automation that goes trhough a range of money transfers (A solution created by the company I work GIMAVE) in a sheet and, once the user gets the 'ok', he/she runs the script and it goes releasing the money transfers to the client's accounts. The transfer volume, daily, is around 150/200 so the automation came as a huge help to the department.


➡ **ERP**: The ERP was created from scratch by me to mitigate an urgent necessity by the Purchase Department: Budget management. 
I) Compras: First module designed and it contains suppliers, products, classes and budgets forms. The system allows to create budgets, compare each other in order to validate which one is more economic and also provides a simples dashboard showing statistics about the budgets from a determined period. 
II) Comercial: Module created to help Sales Department to simulate sells. The user can set the quantity and the price of each product so the system can calculate the revenue. If the simulation has a considerate income user can save it and the information goes to another system, called 'Zoho' to create the contract.
III) Financeiro: My most recent creation. At the moment I'm working on dashboards to both Accounts Payable and Accounts Receivable, in order to help our board take the best decisions in terms of money.


• **Languages**: Python, HTML, CSS, JS, MySQL, ADVPL (Protheus)
