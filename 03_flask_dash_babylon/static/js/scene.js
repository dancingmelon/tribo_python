/// <reference path="babylon.d.ts" />

window.addEventListener('DOMContentLoaded', function() {
    var canvas = document.getElementById('renderCanvas');
    var engine = new BABYLON.Engine(canvas, true);
        
    var createScene = function() {
        var scene = new BABYLON.Scene(engine);
        scene.clearColor = BABYLON.Color3.Gray();
        var camera = new BABYLON.ArcRotateCamera("camera", 0, 0, 0, BABYLON.Vector3.Zero(), scene); //dummy camera to be replaced later

        var door, sample;

        BABYLON.SceneLoader.ImportMesh("", "/static/assets/vacuum_chamber/", "vacuum_chamber.gltf", scene, function(newmeshes) {
            scene.createDefaultCameraOrLight(true, true, true);
            scene.activeCamera.alpha += Math.PI;

            var helper = scene.createDefaultEnvironment({
              createSkybox: false,
              enableGroundMirror: true,
              environmentTexture: '/static/assets/environment.dds',
              cameraExposure: 1.5
            });
            helper.setMainColor(BABYLON.Color3.White());
            
            door = scene.getMeshByName("door");
            sample = scene.getMeshByName("sample");

            initAngle_Y = door.rotationQuaternion.normalize().toEulerAngles().y
            sampleInitPosition_X = sample.position.x;

            // BABYLON GUI
            var advancedTexture = BABYLON.GUI.AdvancedDynamicTexture.CreateFullscreenUI("UI");
		
            var panel = new BABYLON.GUI.StackPanel();
            panel.width = "600px";
            panel.fontSize = "15px";
            panel.horizontalAlignment = BABYLON.GUI.Control.HORIZONTAL_ALIGNMENT_LEFT;
            panel.verticalAlignment = BABYLON.GUI.Control.VERTICAL_ALIGNMENT_TOP;
            panel.paddingLeft = "20px";
            advancedTexture.addControl(panel);
            
            var header = new BABYLON.GUI.TextBlock();
            header.text = "Door rotation value: 0 radian";
            header.height = "40px";
            header.color = "white";
            header.textHorizontalAlignment = BABYLON.GUI.Control.HORIZONTAL_ALIGNMENT_LEFT;
            header.paddingTop = "20px";
            panel.addControl(header); 

            var slider = new BABYLON.GUI.Slider();
            slider.horizontalAlignment = BABYLON.GUI.Control.HORIZONTAL_ALIGNMENT_LEFT;
            slider.minimum = -1.5;
            slider.maximum = 1.7;
            slider.color = "red";
            slider.value = 0;
            slider.height = "20px";
            slider.width = "200px";
            panel.addControl(slider);   

            var header2 = new BABYLON.GUI.TextBlock();
            header2.text = "Sample displacement value: " + sampleInitPosition_X;
            header2.height = "40px";
            header2.color = "white";
            header2.textHorizontalAlignment = BABYLON.GUI.Control.HORIZONTAL_ALIGNMENT_LEFT;
            //header2.paddingTop = "0px";
            panel.addControl(header2); 

            var slider2 = new BABYLON.GUI.Slider();
            slider2.horizontalAlignment = BABYLON.GUI.Control.HORIZONTAL_ALIGNMENT_LEFT;
            slider2.minimum = -5;
            slider2.maximum = 5;
            slider2.color = "red";
            slider2.value = 0;
            slider2.height = "20px";
            slider2.width = "200px";
            panel.addControl(slider2);   
            
            var axis = new BABYLON.Vector3(0, 1, 0);
            slider.onValueChangedObservable.add(function(value) { 
                header.text = "Door rotation value: " + value.toFixed(2) + " radian";
                var angle = value + initAngle_Y;                
                var quaternion = new BABYLON.Quaternion.RotationAxis(axis, angle);
                door.rotationQuaternion = door.rotationQuaternion.add(quaternion).normalize();                
            });
            
            slider2.onValueChangedObservable.add(function(value) {
                var x = sampleInitPosition_X + value;
                sample.position.x = x;
                header2.text = "Sample displacement value: " + value.toFixed(2);
            });

        });
        return scene;
    }

    var scene = createScene();

    engine.runRenderLoop(function() {
        scene.render();
    });
    
    window.addEventListener("resize", function () {
        engine.resize();
    });
});

