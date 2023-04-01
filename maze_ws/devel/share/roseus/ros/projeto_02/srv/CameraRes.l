;; Auto-generated. Do not edit!


(when (boundp 'projeto_02::CameraRes)
  (if (not (find-package "PROJETO_02"))
    (make-package "PROJETO_02"))
  (shadow 'CameraRes (find-package "PROJETO_02")))
(unless (find-package "PROJETO_02::CAMERARES")
  (make-package "PROJETO_02::CAMERARES"))
(unless (find-package "PROJETO_02::CAMERARESREQUEST")
  (make-package "PROJETO_02::CAMERARESREQUEST"))
(unless (find-package "PROJETO_02::CAMERARESRESPONSE")
  (make-package "PROJETO_02::CAMERARESRESPONSE"))

(in-package "ROS")





(defclass projeto_02::CameraResRequest
  :super ros::object
  :slots ())

(defmethod projeto_02::CameraResRequest
  (:init
   (&key
    )
   (send-super :init)
   self)
  (:serialization-length
   ()
   (+
    0
    ))
  (:serialize
   (&optional strm)
   (let ((s (if strm strm
              (make-string-output-stream (send self :serialization-length)))))
     ;;
     (if (null strm) (get-output-stream-string s))))
  (:deserialize
   (buf &optional (ptr- 0))
   ;;
   self)
  )

(defclass projeto_02::CameraResResponse
  :super ros::object
  :slots (_res ))

(defmethod projeto_02::CameraResResponse
  (:init
   (&key
    ((:res __res) 0)
    )
   (send-super :init)
   (setq _res (round __res))
   self)
  (:res
   (&optional __res)
   (if __res (setq _res __res)) _res)
  (:serialization-length
   ()
   (+
    ;; int32 _res
    4
    ))
  (:serialize
   (&optional strm)
   (let ((s (if strm strm
              (make-string-output-stream (send self :serialization-length)))))
     ;; int32 _res
       (write-long _res s)
     ;;
     (if (null strm) (get-output-stream-string s))))
  (:deserialize
   (buf &optional (ptr- 0))
   ;; int32 _res
     (setq _res (sys::peek buf ptr- :integer)) (incf ptr- 4)
   ;;
   self)
  )

(defclass projeto_02::CameraRes
  :super ros::object
  :slots ())

(setf (get projeto_02::CameraRes :md5sum-) "ca16cfbd5443ad97f6cc7ffd6bb67292")
(setf (get projeto_02::CameraRes :datatype-) "projeto_02/CameraRes")
(setf (get projeto_02::CameraRes :request) projeto_02::CameraResRequest)
(setf (get projeto_02::CameraRes :response) projeto_02::CameraResResponse)

(defmethod projeto_02::CameraResRequest
  (:response () (instance projeto_02::CameraResResponse :init)))

(setf (get projeto_02::CameraResRequest :md5sum-) "ca16cfbd5443ad97f6cc7ffd6bb67292")
(setf (get projeto_02::CameraResRequest :datatype-) "projeto_02/CameraResRequest")
(setf (get projeto_02::CameraResRequest :definition-)
      "---
int32 res
")

(setf (get projeto_02::CameraResResponse :md5sum-) "ca16cfbd5443ad97f6cc7ffd6bb67292")
(setf (get projeto_02::CameraResResponse :datatype-) "projeto_02/CameraResResponse")
(setf (get projeto_02::CameraResResponse :definition-)
      "---
int32 res
")



(provide :projeto_02/CameraRes "ca16cfbd5443ad97f6cc7ffd6bb67292")


