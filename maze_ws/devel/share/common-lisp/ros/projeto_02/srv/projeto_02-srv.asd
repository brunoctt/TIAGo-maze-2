
(cl:in-package :asdf)

(defsystem "projeto_02-srv"
  :depends-on (:roslisp-msg-protocol :roslisp-utils )
  :components ((:file "_package")
    (:file "CameraRes" :depends-on ("_package_CameraRes"))
    (:file "_package_CameraRes" :depends-on ("_package"))
  ))