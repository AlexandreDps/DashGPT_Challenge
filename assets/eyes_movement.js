var_setted = false
let rect_left = null
let rect_right = null
let X_left = null
let Y_left = null
let X_right = null
let Y_right = null

setTimeout(function() {
    document.addEventListener("mousemove", (e) => {

        //Centre des yeux
        let left_eye = document.getElementById("left_eye");
        let right_eye = document.getElementById("right_eye");
        if (left_eye != null & right_eye != null ) {
                if (var_setted == false) {
                    rect_left = left_eye.getBoundingClientRect();
                    rect_right = right_eye.getBoundingClientRect();
                    X_left = rect_left.left + (rect_left.width / 2);
                    Y_left = rect_left.top + (rect_left.height / 2);
                    X_right = rect_right.left + (rect_right.width / 2);
                    Y_right = rect_right.top + (rect_right.height / 2);
                    var_setted = true
                }
            
        }

        if (var_setted == true) {
            let x = e.clientX
            let y = e.clientY
            let delta_x_left = X_left - x
            let delta_x_right = X_right - x
            let delta_y_left = Y_left - y
            let delta_y_right = Y_right - y
            distance_left = Math.sqrt( (delta_x_left)**2 + (delta_y_left)**2)
            distance_right = Math.sqrt( (delta_x_right)**2 + (delta_y_right)**2)

            //Calcul d'angle, on imagine un triangle rectangle donc l'hypoténuse est la distance entre les pts
            //Cosinus = Adjacent/Hypoténuse
            adjacent_left = Math.abs(x-X_left)
            angle_left = Math.acos(adjacent_left/distance_left)
            adjacent_right = Math.abs(x-X_right)
            angle_right = Math.acos(adjacent_right/distance_right)
            //Les angles sont en radians
            //On ajuste l'angle selon le plan
            if (delta_x_left>0 & delta_y_left<0) {
                angle_left = 2*Math.PI - angle_left
            }
            else if (delta_x_left<0 & delta_y_left>0) {
                angle_left = Math.PI - angle_left
            }
            else if (delta_x_left<0 & delta_y_left<0) {
                angle_left = Math.PI + angle_left
            }
            //Autre oeil
            if (delta_x_right>0 & delta_y_right<0) {
                angle_right = 2*Math.PI - angle_right
            }
            else if (delta_x_right<0 & delta_y_right>0) {
                angle_right = Math.PI - angle_right
            }
            else if (delta_x_right<0 & delta_y_right<0) {
                angle_right = Math.PI + angle_right
            }
            //Les yeux se déplacent sur un cercle de centre X,Y et de taille 15px
            //On à les coordonnées polaires, il suffit de les convertir en cartésiennes
            max = 15
            if (distance_left>max) {
                distance_left = max
            }
            if (distance_right>max) {
                distance_right = max
            }
            new_x_left = distance_left * Math.cos(angle_left) * -1
            new_y_left = distance_left * Math.sin(angle_left) * -1
            new_x_right = distance_right * Math.cos(angle_right) * -1
            new_y_right = distance_right * Math.sin(angle_right) * -1
            right_eye.style.transform = "translate(" + new_x_right + "px," + new_y_right + "px)";
            left_eye.style.transform = "translate(" + new_x_left + "px," + new_y_left + "px)";
        }
    }
    )
}, 2000);


