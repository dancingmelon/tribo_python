/// <reference path="../src/babylon.d.ts" />

window.addEventListener('DOMContentLoaded', function(){
    var canvas = document.getElementById('renderCanvas');
    var engine = new BABYLON.Engine(canvas, true);

    var scene = new BABYLON.Scene(engine);

    var light = new BABYLON.PointLight("Omni", new BABYLON.Vector3(20,20,100), scene);

    var camera = new BABYLON.ArcRotateCamera("Camera", -Math.PI/3, 1.2, 100, BABYLON.Vector3.Zero(), scene);
    camera.attachControl(canvas, false);


    
    //var assetsManager = new BABYLON.AssetsManager(scene);
    var cube = BABYLON.Mesh.CreateBox("myCube", 10, scene);
    cube.position.x += 30;

    engine.displayLoadingUI();

    BABYLON.SceneLoader.ImportMesh("", "/static/", "monkey.babylon", scene, function(newMeshes) {
        camera.target = newMeshes[0];
        engine.hideLoadingUI();
    }); 

    scene.registerBeforeRender(function() {
        light.position = camera.position;
    });

    // BABYLON.SceneLoader.Load("../", "monkey.babylon", engine, function(scene){
    //     scene.activeCamera.attachControl(canvas);
    //     engine.runRenderLoop(function(){
    //         scene.render();
    //     });
    // });


    // var scene = new BABYLON.Scene(engine);
    // scene.gravity = new BABYLON.Vector3(0, -9.81, 0);
    

    // var cam = new BABYLON.ArcRotateCamera("arcCam", 1, 0.8, 10, new BABYLON.Vector3.Zero(), scene);
    // cam.attachControl(canvas);
    // cam.checkCollisions = true;
    // //cam.applyGravity = true;

    // var cube = BABYLON.Mesh.CreateBox("myCube", 2, scene);
    // cube.position.y += 2;
    // cube.checkCollisions = true;

    // var light = new BABYLON.PointLight("pLight", new BABYLON.Vector3(5, 10, -5), scene);
    // light.diffuse = BABYLON.Color3.Purple();
    
    // var hemi = new BABYLON.HemisphericLight("hLight", BABYLON.Vector3.Zero(), scene);

    // var ground = BABYLON.Mesh.CreateGround("floor", 24, 24, 12, scene);
    // ground.checkCollisions = true;

    // var mat = new BABYLON.StandardMaterial("mat", scene);
    // //scene.collisionsEnabled = true;
 
    engine.runRenderLoop(function(){
        scene.render();
    });

    
    
    // the canvas/window resize event handler
    window.addEventListener('resize', function(){
        engine.resize();
    });
});