def repeat_with_callback(
    max_tries: int, begin_callback: callable, end_callback: callable
):
    def outer_wrapper(target_func):
        def inner_wrapper(*args, **kwargs):
            begin_callback()
            for _ in range(max_tries):
                result = target_func(*args, **kwargs)
            end_callback()

        return inner_wrapper

    return outer_wrapper
