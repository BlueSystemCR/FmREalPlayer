import QtQuick 2.15
import QtQuick.Controls 2.15
import QtQuick.Layouts 1.15

ApplicationWindow {
    id: root
    visible: true
    width: 1200
    height: 800
    title: "Music Manager"
    
    // Propiedades globales para el estado de la aplicación
    property var appController: controller
    property var currentTrack: null
    property bool isPlaying: false
    property int selectedTracks: 0

    // Señales para comunicación entre componentes
    signal trackSelected(var track)
    signal directorySelected(string path)
    signal moveSelectedTracks(string targetPath)

    ColumnLayout {
        anchors.fill: parent
        spacing: 0

        // Barra de herramientas superior
        Rectangle {
            Layout.fillWidth: true
            height: 60
            color: "#252525"
            
            RowLayout {
                anchors.fill: parent
                anchors.margins: 10
                spacing: 15

                Button {
                    text: "Abrir carpeta"
                    onClicked: fileDialog.open()
                }

                TextField {
                    id: searchField
                    Layout.fillWidth: true
                    placeholderText: "Buscar canción..."
                }
            }
        }

        // Lista principal de tracks
        TrackList {
            id: trackList
            Layout.fillWidth: true
            Layout.fillHeight: true
            trackModel: ListModel {}
            onTrackClicked: root.trackSelected(track)
            onSelectionChanged: root.selectedTracks = count
        }

        // Controles de reproducción
        PlayerControls {
            Layout.fillWidth: true
            currentTrack: root.currentTrack ? root.currentTrack.title : "No track selected"
            currentPosition: appController.currentPosition
            duration: appController.currentDuration
            volume: appController.currentVolume
            isPlaying: root.isPlaying
            onPlayPauseClicked: appController.playPause()
            onPreviousClicked: appController.previousTrack()
            onNextClicked: appController.nextTrack()
            onSeekRequested: appController.seek(position)
            onVolumeChanged: appController.setVolume(volume)
        }
    }

    // Diálogo para selección de archivos
    FileDialog {
        id: fileDialog
        title: "Seleccionar carpeta de música"
        folder: StandardPaths.writableLocation(StandardPaths.MusicLocation)
        selectFolder: true
        onAccepted: root.directorySelected(fileDialog.fileUrl)
    }

    // Conexiones con el backend
    Connections {
        target: appController
        
        function onTrackChanged(track) {
            root.currentTrack = track
        }
        
        function onPlaybackStateChanged(playing) {
            root.isPlaying = playing
        }
        
        function onError(message) {
            errorDialog.text = message
            errorDialog.open()
        }
    }

    // Diálogo de error
    Dialog {
        id: errorDialog
        title: "Error"
        standardButtons: Dialog.Ok
        Text {
            text: errorDialog.text
        }
    }
}