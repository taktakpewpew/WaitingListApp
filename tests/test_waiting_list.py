from app.models import WaitingListEntry


def test_join_waiting_list_based_on_available_stock(client, test_session, test_user, test_setup_without_inventory, test_inventory):
    response = client.post(
        "/waiting-list/join",
        json={
            "user_id": test_user.id,
            "offer_id": test_setup_without_inventory['offer'].offer_id,
            "representation_id": test_setup_without_inventory['representation'].id,
            "quantity": 5
        }
    )

    #user should be able to join waiting_list only if there is no stock
    if test_inventory.available_stock == 0:
        assert response.status_code == 201
        created = test_session.query(WaitingListEntry).filter(WaitingListEntry.user_id == test_user.id).one()
        assert created.offer_id == test_setup_without_inventory['offer'].offer_id and created.representation_id == test_setup_without_inventory['representation'].id
    else:
        assert response.status_code == 400
        assert response.json()["detail"] == "Tickets are still available — no need to join the waiting list."

def test_inventory_not_found(client, test_user, test_setup_without_inventory):
    response = client.post(
        "/waiting-list/join",
        json={
            "user_id": test_user.id,
            "offer_id": test_setup_without_inventory['offer'].offer_id,
            "representation_id": test_setup_without_inventory['representation'].id,
            "quantity": 5
        }
    )
    assert response.status_code == 404
    assert response.json()["detail"] == "Inventory not found."

def test_user_already_in_waiting_list(client, test_session, test_user, test_setup_without_inventory, test_inventory):
    #add waiting list entry for user
    test_session.add(WaitingListEntry(user_id=test_user.id, representation_id=test_setup_without_inventory['representation'].id,
                                      offer_id=test_setup_without_inventory['offer'].offer_id, quantity=12))
    test_session.commit()

    response = client.post(
        "/waiting-list/join",
        json={
            "user_id": test_user.id,
            "offer_id": test_setup_without_inventory['offer'].offer_id,
            "representation_id": test_setup_without_inventory['representation'].id,
            "quantity": 5
        }
    )
    if test_inventory.available_stock == 0:
        assert response.status_code == 400
        assert response.json()["detail"] == "User is already on the waiting list."
    else:
        assert response.status_code == 400
        assert response.json()["detail"] == "Tickets are still available — no need to join the waiting list."

#TODO: add more tests for other exceptions

#TODO: add tests for other routes