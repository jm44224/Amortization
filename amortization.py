from amortization_view import Amort_View
from amortization_model import Amort_Model
from amortization_controller import Amort_Controller

# initializes model and view, and passes to controller
amort_model = Amort_Model()
amort_view = Amort_View()
amort_controller = Amort_Controller(amort_model, amort_view)
# starts the amortization user interface
amort_controller.RunAmort()

