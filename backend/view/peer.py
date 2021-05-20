from flask import Blueprint, request
from backend.model.blockchain import blockchain
from backend.model.http_result import HttpResult
from simchain import Peer

app_peer = Blueprint("peer", __name__)


@app_peer.route('/network/peer/list')
def get_peer_info_list():
    peers = blockchain.get_peers()
    peers_info = []
    count = 0
    for peer in peers:
        # 后续根据具体所需信息进行完善
        info = {
            "id": count,
            "ipv4": peer.ipv4,
            "balance": peer.get_balance(),
            "addr": peer.addr
        }
        peers_info.append(info)
        count = count + 1

    return HttpResult.success_result(peers_info)


@app_peer.route('/network/peer/detail')
def get_peer_info_detail():
    peer_id = int(request.args.get("pid"))
    peer: Peer = blockchain.get_peers()[peer_id]
    info = {
        "id": peer_id,
        "ipv4": peer.ipv4,
        "balance": peer.get_balance(),
        "addr": peer.addr
    }
    return HttpResult.success_result(info)


@app_peer.route('/network/peer/add')
def network_peer_add():
    peer = blockchain.net.add_peer()
    info = {
        "id": peer.pid,
        "ipv4": peer.ipv4,
        "balance": peer.get_balance(),
        "addr": peer.addr
    }
    return HttpResult.success_result(info)


@app_peer.route('/network/peer/utxo')
def get_peer_utxo():
    peer_id = int(request.args.get("peer_id"))

    peers = blockchain.get_peers()
    utxos = peers[peer_id].get_utxo()
    data = []
    for each in utxos:
        vout = each.vout
        pointer = each.pointer
        each_data = {
            "vout_addr": vout.to_addr,
            "vout_value": vout.value,
            "tx_id": pointer.tx_id,
            "tx_vout_n": pointer.n
        }
        data.append(each_data)

    return HttpResult.success_result(data)


@app_peer.route('/network/peer/utxo/unconfirm')
def get_peer_utxo_unconfirmed():
    peer_id = int(request.args.get("peer_id"))

    peers = blockchain.get_peers()
    utxos = peers[peer_id].get_unconfirmed_utxo()
    data = []
    for each in utxos:
        vout = each.vout
        pointer = each.pointer
        each_data = {
            "vout_addr": vout.to_addr,
            "vout_value": vout.value,
            "tx_id": pointer.tx_id,
            "tx_vout_n": pointer.n
        }
        data.append(each_data)

    return HttpResult.success_result(data)


@app_peer.route('/network/peer/utxo/confirm')
def get_peer_utxo_confirmed():
    peer_id = int(request.args.get("peer_id"))

    peers = blockchain.get_peers()
    utxos = peers[peer_id].get_confirmed_utxo()
    data = []
    for each in utxos:
        vout = each.vout
        pointer = each.pointer
        each_data = {
            "vout_addr": vout.to_addr,
            "vout_value": vout.value,
            "tx_id": pointer.tx_id,
            "tx_vout_n": pointer.n
        }
        data.append(each_data)

    return HttpResult.success_result(data)
