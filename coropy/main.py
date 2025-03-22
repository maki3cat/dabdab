
from basic import _Eventloop, common_workflow

if __name__ == "__main__":
    c_runtime = _Eventloop.get_current_eventloop()
    c_runtime.call_now(None, common_workflow, "GLOVER")
    c_runtime.run()
