IDS = [
    "login",
    "loginDemo",
    "viewAccount",
    "viewStatement",
    "viewPendingDocs",
    "createRublePayment",
    "createInstantPayment",
    "createEripPayment",
    "createSalaryPayment",
    "createCurrencyPayment",
    "createRussiaPayment",
    "viewDocument",
    "editDocument",
    "deleteDocument",
    "repeatPayment",
    "printDocument",
    "openDeposit",
    "openNewAccount",
    "acquiringService",
    "salaryProject",
    "openSupportChat",
    "openSupportChatFromInfo",
    "changePassword",
    "configureNotifications",
    "findBranch",
    "viewFxRates",
    "logout"
]

def control_button_check_node(state):
    if state["button"] == "":
        return {
            "button_correct": True,
        }
    if state["button"] in IDS:
        return {
            "button_correct": True,
        }
    else:
        return {
            "button_correct": False,
            "button": ""
        }