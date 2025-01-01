import QtQuick 2.15
import QtQuick.Controls 2.15
import QtQuick.Layouts 1.15

Rectangle {
    id: trackListRoot
    color: "#2b2b2b"

    property var trackModel
    property int selectedCount: 0

    function selectAllTracks(checked) {
        for (var i = 0; i < trackModel.count; i++) {
            trackModel.get(i).isSelected = checked
        }
        updateSelectedCount()
    }

    function updateSelectedCount() {
        var count = 0
        for (var i = 0; i < trackModel.count; i++) {
            if (trackModel.get(i).isSelected) {
                count++
            }
        }
        selectedCount = count
    }

    ColumnLayout {
        anchors.fill: parent
        spacing: 0

        // Cabecera de columnas
        Rectangle {
            Layout.fillWidth: true
            height: 40
            color: "#333333"
            
            RowLayout {
                anchors.fill: parent
                anchors.margins: 10
                spacing: 10

                CheckBox {
                    id: selectAllCheckbox
                    onCheckedChanged: selectAllTracks(checked)
                }

                HeaderLabel { 
                    text: "Título"
                    Layout.fillWidth: true
                    onClicked: sortByColumn("title")
                }

                HeaderLabel { 
                    text: "Artista" 
                    Layout.fillWidth: true
                    onClicked: sortByColumn("artist")
                }

                HeaderLabel { 
                    text: "Álbum"
                    Layout.fillWidth: true
                    onClicked: sortByColumn("album")
                }

                HeaderLabel { 
                    text: "Año"
                    Layout.preferredWidth: 80
                    onClicked: sortByColumn("year")
                }

                HeaderLabel { 
                    text: "Duración"
                    Layout.preferredWidth: 100
                    onClicked: sortByColumn("duration")
                }
            }
        }

        // Lista de tracks
        ListView {
            id: trackListView
            Layout.fillWidth: true
            Layout.fillHeight: true
            clip: true
            model: trackModel
            delegate: TrackDelegate {
                width: trackListView.width
                onSelectedChanged: updateSelectedCount()
            }

            ScrollBar.vertical: ScrollBar { }
        }

        // Barra de estado
        Rectangle {
            Layout.fillWidth: true
            height: 30
            color: "#333333"
            
            RowLayout {
                anchors.fill: parent
                anchors.margins: 10
                
                Text {
                    text: selectedCount + " pistas seleccionadas"
                    color: "white"
                }
            }
        }
    }

    function sortByColumn(column) {
        // Implementar lógica de ordenamiento
    }
}