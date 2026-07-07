from app.models.execution import ExecutionContext


def test_context():

    ctx = ExecutionContext("Ventas")

    ctx.set_variable("anio", 2026)

    assert ctx.get_variable("anio") == 2026

    ctx.log("Pipeline iniciado")

    assert len(ctx.logs) == 1

    ctx.set_dataframe("ventas", "dummy")

    assert ctx.get_dataframe("ventas") == "dummy"