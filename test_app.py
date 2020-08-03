import json


def test_codes(app, client):
    res = client.get("/analyze")
    assert res.status_code == 405

    res = client.post(
        "/analyze",
        data=json.dumps(
            dict(input="An order must be packaged", verb="ship", noun="order")
        ),
        content_type="application/json",
    )
    assert res.status_code == 200
    expected = {"result": "To ship order, the order must be packaged."}
    assert expected == json.loads(res.get_data(as_text=True))

    res = client.post(
        "/analyze",
        data=json.dumps(
            dict(input="A contract should be signed.", verb="send", noun="invoice")
        ),
        content_type="application/json",
    )
    expected = {"result": "To send invoice, the contract should be signed."}
    assert expected == json.loads(res.get_data(as_text=True))


def test_output(app, client):
    res = client.post(
        "/analyze",
        data=json.dumps(
            dict(input="An order must be packaged", verb="ship", noun="order")
        ),
        content_type="application/json",
    )
    expected = {"result": "To ship order, the order must be packaged."}
    assert expected == json.loads(res.get_data(as_text=True))

    res = client.post(
        "/analyze",
        data=json.dumps(
            dict(input="A contract should be signed.", verb="send", noun="invoice")
        ),
        content_type="application/json",
    )
    expected = {"result": "To send invoice, the contract should be signed."}
    assert expected == json.loads(res.get_data(as_text=True))


def test_branch(app, client):
    res = client.post(
        "/analyze",
        data=json.dumps(
            dict(input="An order must be packaged and paid", verb="ship", noun="order")
        ),
        content_type="application/json",
    )
    expected = {"result": "To ship order, the order must be packaged and paid."}
    assert expected == json.loads(res.get_data(as_text=True))


def test_additional_model(app, client):
    res = client.post(
        "/analyze",
        data=json.dumps(
            dict(input="An order must be properly packaged", verb="ship", noun="order")
        ),
        content_type="application/json",
    )
    expected = {"result": "To ship order, the order must be properly packaged."}
    assert expected == json.loads(res.get_data(as_text=True))


def test_wrong_data(app, client):
    res = client.post(
        "/analyze",
        data=json.dumps(
            dict(
                input="An order must be properly packaged",
                noun="order",
                adverb="thoroughly",
            )
        ),
        content_type="application/json",
    )
    expected = {"error": "Wrong data parameters"}
    assert expected == json.loads(res.get_data(as_text=True))

