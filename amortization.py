from amortization_view import AmortizationView
from amortization_model import AmortizationModel
from amortization_controller import AmortizationController

AmortizationController(AmortizationModel(), AmortizationView()).run_amortization()

