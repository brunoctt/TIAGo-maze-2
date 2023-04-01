; Auto-generated. Do not edit!


(cl:in-package projeto_02-srv)


;//! \htmlinclude CameraRes-request.msg.html

(cl:defclass <CameraRes-request> (roslisp-msg-protocol:ros-message)
  ()
)

(cl:defclass CameraRes-request (<CameraRes-request>)
  ())

(cl:defmethod cl:initialize-instance :after ((m <CameraRes-request>) cl:&rest args)
  (cl:declare (cl:ignorable args))
  (cl:unless (cl:typep m 'CameraRes-request)
    (roslisp-msg-protocol:msg-deprecation-warning "using old message class name projeto_02-srv:<CameraRes-request> is deprecated: use projeto_02-srv:CameraRes-request instead.")))
(cl:defmethod roslisp-msg-protocol:serialize ((msg <CameraRes-request>) ostream)
  "Serializes a message object of type '<CameraRes-request>"
)
(cl:defmethod roslisp-msg-protocol:deserialize ((msg <CameraRes-request>) istream)
  "Deserializes a message object of type '<CameraRes-request>"
  msg
)
(cl:defmethod roslisp-msg-protocol:ros-datatype ((msg (cl:eql '<CameraRes-request>)))
  "Returns string type for a service object of type '<CameraRes-request>"
  "projeto_02/CameraResRequest")
(cl:defmethod roslisp-msg-protocol:ros-datatype ((msg (cl:eql 'CameraRes-request)))
  "Returns string type for a service object of type 'CameraRes-request"
  "projeto_02/CameraResRequest")
(cl:defmethod roslisp-msg-protocol:md5sum ((type (cl:eql '<CameraRes-request>)))
  "Returns md5sum for a message object of type '<CameraRes-request>"
  "ca16cfbd5443ad97f6cc7ffd6bb67292")
(cl:defmethod roslisp-msg-protocol:md5sum ((type (cl:eql 'CameraRes-request)))
  "Returns md5sum for a message object of type 'CameraRes-request"
  "ca16cfbd5443ad97f6cc7ffd6bb67292")
(cl:defmethod roslisp-msg-protocol:message-definition ((type (cl:eql '<CameraRes-request>)))
  "Returns full string definition for message of type '<CameraRes-request>"
  (cl:format cl:nil "~%~%"))
(cl:defmethod roslisp-msg-protocol:message-definition ((type (cl:eql 'CameraRes-request)))
  "Returns full string definition for message of type 'CameraRes-request"
  (cl:format cl:nil "~%~%"))
(cl:defmethod roslisp-msg-protocol:serialization-length ((msg <CameraRes-request>))
  (cl:+ 0
))
(cl:defmethod roslisp-msg-protocol:ros-message-to-list ((msg <CameraRes-request>))
  "Converts a ROS message object to a list"
  (cl:list 'CameraRes-request
))
;//! \htmlinclude CameraRes-response.msg.html

(cl:defclass <CameraRes-response> (roslisp-msg-protocol:ros-message)
  ((res
    :reader res
    :initarg :res
    :type cl:integer
    :initform 0))
)

(cl:defclass CameraRes-response (<CameraRes-response>)
  ())

(cl:defmethod cl:initialize-instance :after ((m <CameraRes-response>) cl:&rest args)
  (cl:declare (cl:ignorable args))
  (cl:unless (cl:typep m 'CameraRes-response)
    (roslisp-msg-protocol:msg-deprecation-warning "using old message class name projeto_02-srv:<CameraRes-response> is deprecated: use projeto_02-srv:CameraRes-response instead.")))

(cl:ensure-generic-function 'res-val :lambda-list '(m))
(cl:defmethod res-val ((m <CameraRes-response>))
  (roslisp-msg-protocol:msg-deprecation-warning "Using old-style slot reader projeto_02-srv:res-val is deprecated.  Use projeto_02-srv:res instead.")
  (res m))
(cl:defmethod roslisp-msg-protocol:serialize ((msg <CameraRes-response>) ostream)
  "Serializes a message object of type '<CameraRes-response>"
  (cl:let* ((signed (cl:slot-value msg 'res)) (unsigned (cl:if (cl:< signed 0) (cl:+ signed 4294967296) signed)))
    (cl:write-byte (cl:ldb (cl:byte 8 0) unsigned) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 8) unsigned) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 16) unsigned) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 24) unsigned) ostream)
    )
)
(cl:defmethod roslisp-msg-protocol:deserialize ((msg <CameraRes-response>) istream)
  "Deserializes a message object of type '<CameraRes-response>"
    (cl:let ((unsigned 0))
      (cl:setf (cl:ldb (cl:byte 8 0) unsigned) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 8) unsigned) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 16) unsigned) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 24) unsigned) (cl:read-byte istream))
      (cl:setf (cl:slot-value msg 'res) (cl:if (cl:< unsigned 2147483648) unsigned (cl:- unsigned 4294967296))))
  msg
)
(cl:defmethod roslisp-msg-protocol:ros-datatype ((msg (cl:eql '<CameraRes-response>)))
  "Returns string type for a service object of type '<CameraRes-response>"
  "projeto_02/CameraResResponse")
(cl:defmethod roslisp-msg-protocol:ros-datatype ((msg (cl:eql 'CameraRes-response)))
  "Returns string type for a service object of type 'CameraRes-response"
  "projeto_02/CameraResResponse")
(cl:defmethod roslisp-msg-protocol:md5sum ((type (cl:eql '<CameraRes-response>)))
  "Returns md5sum for a message object of type '<CameraRes-response>"
  "ca16cfbd5443ad97f6cc7ffd6bb67292")
(cl:defmethod roslisp-msg-protocol:md5sum ((type (cl:eql 'CameraRes-response)))
  "Returns md5sum for a message object of type 'CameraRes-response"
  "ca16cfbd5443ad97f6cc7ffd6bb67292")
(cl:defmethod roslisp-msg-protocol:message-definition ((type (cl:eql '<CameraRes-response>)))
  "Returns full string definition for message of type '<CameraRes-response>"
  (cl:format cl:nil "int32 res~%~%~%"))
(cl:defmethod roslisp-msg-protocol:message-definition ((type (cl:eql 'CameraRes-response)))
  "Returns full string definition for message of type 'CameraRes-response"
  (cl:format cl:nil "int32 res~%~%~%"))
(cl:defmethod roslisp-msg-protocol:serialization-length ((msg <CameraRes-response>))
  (cl:+ 0
     4
))
(cl:defmethod roslisp-msg-protocol:ros-message-to-list ((msg <CameraRes-response>))
  "Converts a ROS message object to a list"
  (cl:list 'CameraRes-response
    (cl:cons ':res (res msg))
))
(cl:defmethod roslisp-msg-protocol:service-request-type ((msg (cl:eql 'CameraRes)))
  'CameraRes-request)
(cl:defmethod roslisp-msg-protocol:service-response-type ((msg (cl:eql 'CameraRes)))
  'CameraRes-response)
(cl:defmethod roslisp-msg-protocol:ros-datatype ((msg (cl:eql 'CameraRes)))
  "Returns string type for a service object of type '<CameraRes>"
  "projeto_02/CameraRes")