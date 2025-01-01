import QtQuick 2.15
import QtQuick.Controls 2.15

Text {
    property alias text: label.text
    signal clicked()

    id: label
    color: "white"
    font.bold: true
    font.pixelSize: 12

    MouseArea {
        anchors.fill: parent
        onClicked: parent.clicked()
        cursorShape: Qt.PointingHandCursor
    }
}