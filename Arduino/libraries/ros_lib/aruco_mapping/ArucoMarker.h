#ifndef _ROS_aruco_mapping_ArucoMarker_h
#define _ROS_aruco_mapping_ArucoMarker_h

#include <stdint.h>
#include <string.h>
#include <stdlib.h>
#include "ros/msg.h"
#include "std_msgs/Header.h"
#include "geometry_msgs/Pose.h"

namespace aruco_mapping
{

  class ArucoMarker : public ros::Msg
  {
    public:
      typedef std_msgs::Header _header_type;
      _header_type header;
      typedef bool _marker_visibile_type;
      _marker_visibile_type marker_visibile;
      typedef int32_t _num_of_visible_markers_type;
      _num_of_visible_markers_type num_of_visible_markers;
      typedef geometry_msgs::Pose _global_camera_pose_type;
      _global_camera_pose_type global_camera_pose;
      uint32_t marker_ids_length;
      typedef int32_t _marker_ids_type;
      _marker_ids_type st_marker_ids;
      _marker_ids_type * marker_ids;
      uint32_t global_marker_poses_length;
      typedef geometry_msgs::Pose _global_marker_poses_type;
      _global_marker_poses_type st_global_marker_poses;
      _global_marker_poses_type * global_marker_poses;

    ArucoMarker():
      header(),
      marker_visibile(0),
      num_of_visible_markers(0),
      global_camera_pose(),
      marker_ids_length(0), marker_ids(NULL),
      global_marker_poses_length(0), global_marker_poses(NULL)
    {
    }

    virtual int serialize(unsigned char *outbuffer) const
    {
      int offset = 0;
      offset += this->header.serialize(outbuffer + offset);
      union {
        bool real;
        uint8_t base;
      } u_marker_visibile;
      u_marker_visibile.real = this->marker_visibile;
      *(outbuffer + offset + 0) = (u_marker_visibile.base >> (8 * 0)) & 0xFF;
      offset += sizeof(this->marker_visibile);
      union {
        int32_t real;
        uint32_t base;
      } u_num_of_visible_markers;
      u_num_of_visible_markers.real = this->num_of_visible_markers;
      *(outbuffer + offset + 0) = (u_num_of_visible_markers.base >> (8 * 0)) & 0xFF;
      *(outbuffer + offset + 1) = (u_num_of_visible_markers.base >> (8 * 1)) & 0xFF;
      *(outbuffer + offset + 2) = (u_num_of_visible_markers.base >> (8 * 2)) & 0xFF;
      *(outbuffer + offset + 3) = (u_num_of_visible_markers.base >> (8 * 3)) & 0xFF;
      offset += sizeof(this->num_of_visible_markers);
      offset += this->global_camera_pose.serialize(outbuffer + offset);
      *(outbuffer + offset + 0) = (this->marker_ids_length >> (8 * 0)) & 0xFF;
      *(outbuffer + offset + 1) = (this->marker_ids_length >> (8 * 1)) & 0xFF;
      *(outbuffer + offset + 2) = (this->marker_ids_length >> (8 * 2)) & 0xFF;
      *(outbuffer + offset + 3) = (this->marker_ids_length >> (8 * 3)) & 0xFF;
      offset += sizeof(this->marker_ids_length);
      for( uint32_t i = 0; i < marker_ids_length; i++){
      union {
        int32_t real;
        uint32_t base;
      } u_marker_idsi;
      u_marker_idsi.real = this->marker_ids[i];
      *(outbuffer + offset + 0) = (u_marker_idsi.base >> (8 * 0)) & 0xFF;
      *(outbuffer + offset + 1) = (u_marker_idsi.base >> (8 * 1)) & 0xFF;
      *(outbuffer + offset + 2) = (u_marker_idsi.base >> (8 * 2)) & 0xFF;
      *(outbuffer + offset + 3) = (u_marker_idsi.base >> (8 * 3)) & 0xFF;
      offset += sizeof(this->marker_ids[i]);
      }
      *(outbuffer + offset + 0) = (this->global_marker_poses_length >> (8 * 0)) & 0xFF;
      *(outbuffer + offset + 1) = (this->global_marker_poses_length >> (8 * 1)) & 0xFF;
      *(outbuffer + offset + 2) = (this->global_marker_poses_length >> (8 * 2)) & 0xFF;
      *(outbuffer + offset + 3) = (this->global_marker_poses_length >> (8 * 3)) & 0xFF;
      offset += sizeof(this->global_marker_poses_length);
      for( uint32_t i = 0; i < global_marker_poses_length; i++){
      offset += this->global_marker_poses[i].serialize(outbuffer + offset);
      }
      return offset;
    }

    virtual int deserialize(unsigned char *inbuffer)
    {
      int offset = 0;
      offset += this->header.deserialize(inbuffer + offset);
      union {
        bool real;
        uint8_t base;
      } u_marker_visibile;
      u_marker_visibile.base = 0;
      u_marker_visibile.base |= ((uint8_t) (*(inbuffer + offset + 0))) << (8 * 0);
      this->marker_visibile = u_marker_visibile.real;
      offset += sizeof(this->marker_visibile);
      union {
        int32_t real;
        uint32_t base;
      } u_num_of_visible_markers;
      u_num_of_visible_markers.base = 0;
      u_num_of_visible_markers.base |= ((uint32_t) (*(inbuffer + offset + 0))) << (8 * 0);
      u_num_of_visible_markers.base |= ((uint32_t) (*(inbuffer + offset + 1))) << (8 * 1);
      u_num_of_visible_markers.base |= ((uint32_t) (*(inbuffer + offset + 2))) << (8 * 2);
      u_num_of_visible_markers.base |= ((uint32_t) (*(inbuffer + offset + 3))) << (8 * 3);
      this->num_of_visible_markers = u_num_of_visible_markers.real;
      offset += sizeof(this->num_of_visible_markers);
      offset += this->global_camera_pose.deserialize(inbuffer + offset);
      uint32_t marker_ids_lengthT = ((uint32_t) (*(inbuffer + offset))); 
      marker_ids_lengthT |= ((uint32_t) (*(inbuffer + offset + 1))) << (8 * 1); 
      marker_ids_lengthT |= ((uint32_t) (*(inbuffer + offset + 2))) << (8 * 2); 
      marker_ids_lengthT |= ((uint32_t) (*(inbuffer + offset + 3))) << (8 * 3); 
      offset += sizeof(this->marker_ids_length);
      if(marker_ids_lengthT > marker_ids_length)
        this->marker_ids = (int32_t*)realloc(this->marker_ids, marker_ids_lengthT * sizeof(int32_t));
      marker_ids_length = marker_ids_lengthT;
      for( uint32_t i = 0; i < marker_ids_length; i++){
      union {
        int32_t real;
        uint32_t base;
      } u_st_marker_ids;
      u_st_marker_ids.base = 0;
      u_st_marker_ids.base |= ((uint32_t) (*(inbuffer + offset + 0))) << (8 * 0);
      u_st_marker_ids.base |= ((uint32_t) (*(inbuffer + offset + 1))) << (8 * 1);
      u_st_marker_ids.base |= ((uint32_t) (*(inbuffer + offset + 2))) << (8 * 2);
      u_st_marker_ids.base |= ((uint32_t) (*(inbuffer + offset + 3))) << (8 * 3);
      this->st_marker_ids = u_st_marker_ids.real;
      offset += sizeof(this->st_marker_ids);
        memcpy( &(this->marker_ids[i]), &(this->st_marker_ids), sizeof(int32_t));
      }
      uint32_t global_marker_poses_lengthT = ((uint32_t) (*(inbuffer + offset))); 
      global_marker_poses_lengthT |= ((uint32_t) (*(inbuffer + offset + 1))) << (8 * 1); 
      global_marker_poses_lengthT |= ((uint32_t) (*(inbuffer + offset + 2))) << (8 * 2); 
      global_marker_poses_lengthT |= ((uint32_t) (*(inbuffer + offset + 3))) << (8 * 3); 
      offset += sizeof(this->global_marker_poses_length);
      if(global_marker_poses_lengthT > global_marker_poses_length)
        this->global_marker_poses = (geometry_msgs::Pose*)realloc(this->global_marker_poses, global_marker_poses_lengthT * sizeof(geometry_msgs::Pose));
      global_marker_poses_length = global_marker_poses_lengthT;
      for( uint32_t i = 0; i < global_marker_poses_length; i++){
      offset += this->st_global_marker_poses.deserialize(inbuffer + offset);
        memcpy( &(this->global_marker_poses[i]), &(this->st_global_marker_poses), sizeof(geometry_msgs::Pose));
      }
     return offset;
    }

    const char * getType(){ return "aruco_mapping/ArucoMarker"; };
    const char * getMD5(){ return "e73493d4620efa2f38fe39e7896d4192"; };

  };

}
#endif