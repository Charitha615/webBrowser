import QtQuick 2.15
import QtQuick.Controls 2.15
import QtWebEngine 1.10

ApplicationWindow {
    visible: true
    width: 800
    height: 600
    title: "Modern Web Browser" // Set the window title here

    WebView {
        id: webview
        anchors.fill: parent
        url: "https://www.google.com"
    }

    Item {
        anchors.fill: parent
        Rectangle {
            id: topBar
            width: parent.width
            height: 50
            color: "#0078D7"

            TextField {
                id: urlBar
                width: parent.width - backBtn.width - forwardBtn.width - reloadBtn.width - homeBtn.width - stopBtn.width - 10
                height: 30
                anchors.verticalCenter: parent.verticalCenter
                anchors.left: parent.left
                placeholderText: "Enter URL"
                onReturnPressed: webview.url = urlBar.text
            }

            Button {
                id: backBtn
                text: "<"
                width: 40
                height: 30
                anchors.verticalCenter: parent.verticalCenter
                anchors.left: parent.left
                onClicked: webview.goBack()
            }

            Button {
                id: forwardBtn
                text: ">"
                width: 40
                height: 30
                anchors.verticalCenter: parent.verticalCenter
                anchors.left: backBtn.right
                onClicked: webview.goForward()
            }

            Button {
                id: reloadBtn
                text: "⟳"
                width: 40
                height: 30
                anchors.verticalCenter: parent.verticalCenter
                anchors.left: forwardBtn.right
                onClicked: webview.reload()
            }

            Button {
                id: homeBtn
                text: "Home"
                width: 80
                height: 30
                anchors.verticalCenter: parent.verticalCenter
                anchors.left: reloadBtn.right
                onClicked: webview.url = "https://www.google.com"
            }

            Button {
                id: stopBtn
                text: "Stop"
                width: 60
                height: 30
                anchors.verticalCenter: parent.verticalCenter
                anchors.left: homeBtn.right
                onClicked: webview.stop()
            }
        }
    }
}
