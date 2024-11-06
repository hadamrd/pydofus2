from flask import Flask, jsonify, render_template
from flask_socketio import SocketIO

from pydofus2.com.ankamagames.jerakine.network.NetworkMessage import NetworkMessage
from pydofus2.sniffer.network.DofusSniffer import DofusSniffer


class DofusSnifferApp:
    def __init__(self):
        self.app = Flask(__name__)
        self.socketio = SocketIO(self.app)
        self.sniffer: DofusSniffer = None
        self.setup_routes()

    def handle_new_message(self, conn_id: str, msg: NetworkMessage, from_client: bool):
        # Only process marketplace-related messages
        bidhouse_filter = {
            "TextInformationMessage",  # tells us info about sold items
            "ExchangeBidHouseItemRemoveOkMessage",  # means some item was sold or removed after modification
            "NpcGenericActionRequestMessage",
            # Search & Price Messages
            "ExchangeBidHouseSearchMessage",
            "ExchangeBidHousePriceMessage",
            "ExchangeBidPriceForSellerMessage",
            "ExchangeTypesItemsExchangerDescriptionForUserMessage",
            # Selling Messages
            "NpcGenericActionRequestMessage",  # Opening sell mode
            "ExchangeStartedBidSellerMessage",  # Sell mode started
            "ExchangeObjectMovePricedMessage",  # Put item for sale
            "ExchangeBidHouseItemAddOkMessage",  # Sale confirmed
            "ExchangeBidHouseInListUpdatedMessage",  # Market listing updated
            # Update Messages
            "ExchangeObjectModifyPricedMessage",
            # Inventory Updates
            "ObjectDeletedMessage",
            "ObjectQuantityMessage",
            "KamasUpdateMessage",
            "InventoryWeightMessage",
        }

        msg.__class__.__name__
        # if msg_type in bidhouse_filter:
        msg_json = self.sniffer.messagesRecord[conn_id][-1]
        client, server = conn_id.split(" <-> ")
        _, _, client_port = client.split(":")
        _, server_host, _ = server.split(":")
        connection_id = f"{client_port}::{server_host}"
        self.socketio.emit("new_message", {"conn_id": connection_id, "message": msg_json, "from_client": from_client})

    def handle_sniffer_crash(self, error_trace):
        print(f"Sniffer crashed with error: {error_trace}")
        self.socketio.emit("sniffer_crash", {"error": error_trace})

    @property
    def is_sniffer_running(self):
        return self.sniffer and self.sniffer.running.is_set()

    def setup_routes(self):
        @self.app.route("/")
        def index():
            return render_template("index.html")

        @self.app.route("/sniffer_status")
        def status():
            return jsonify({"sniffer_status": "running" if self.is_sniffer_running else "stopped"})

        @self.app.route("/toggle_sniffer", methods=["POST"])
        def toggle_sniffer():
            action = "stopped" if self.is_sniffer_running else "started"
            if self.is_sniffer_running:
                self.sniffer.stop()
                self.sniffer = None
            else:
                self.sniffer = DofusSniffer(
                    "DofusSnifferApp", on_message=self.handle_new_message, on_crash=self.handle_sniffer_crash
                )
                self.sniffer.start()
            return jsonify({"status": "success", "message": f"Sniffer {action}", "action": action})

    def run(self, debug=True, port=8700):
        self.socketio.run(self.app, debug=debug, port=port)


if __name__ == "__main__":
    app = DofusSnifferApp()
    app.run(debug=False)
