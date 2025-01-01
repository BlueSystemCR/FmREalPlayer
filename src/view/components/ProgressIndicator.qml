import QtQuick 2.15
import QtQuick.Controls 2.15

Rectangle {
    id: root
    visible: false
    anchors.centerIn: parent
    width: 200
    height: 100
    color: "#2b2b2b"
    radius: 5

    property string message: "Procesando..."
    property real progress: 0

    Column {
        anchors.centerIn: parent
        spacing: 10

        Text {
            text: root.message
            color: "white"
            font.pixelSize: 14
            anchors.horizontalCenter: parent.horizontalCenter
        }

        ProgressBar {
            width: 180
            value: root.progress
            from: 0
            to: 1
        }
    }

    function show(message) {
        root.message = message
        root.progress = 0
        root.visible = true
    }

    function updateProgress(value) {
        root.progress = value
    }

    function hide() {
        root.visible = false
    }
}