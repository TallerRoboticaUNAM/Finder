#ifndef _ROS_SERVICE_RecognizeGazeboObject_h
#define _ROS_SERVICE_RecognizeGazeboObject_h
#include <stdint.h>
#include <string.h>
#include <stdlib.h>
#include "ros/msg.h"

namespace gazebo_test_tools
{

static const char RECOGNIZEGAZEBOOBJECT[] = "gazebo_test_tools/RecognizeGazeboObject";

  class RecognizeGazeboObjectRequest : public ros::Msg
  {
    public:
      const char* name;
      bool republish;

    RecognizeGazeboObjectRequest():
      name(""),
      republish(0)
    {
    }

    virtual int serialize(unsigned char *outbuffer) const
    {
      int offset = 0;
      uint32_t length_name = strlen(this->name);
      memcpy(outbuffer + offset, &length_name, sizeof(uint32_t));
      offset += 4;
      memcpy(outbuffer + offset, this->name, length_name);
      offset += length_name;
      union {
        bool real;
        uint8_t base;
      } u_republish;
      u_republish.real = this->republish;
      *(outbuffer + offset + 0) = (u_republish.base >> (8 * 0)) & 0xFF;
      offset += sizeof(this->republish);
      return offset;
    }

    virtual int deserialize(unsigned char *inbuffer)
    {
      int offset = 0;
      uint32_t length_name;
      memcpy(&length_name, (inbuffer + offset), sizeof(uint32_t));
      offset += 4;
      for(unsigned int k= offset; k< offset+length_name; ++k){
          inbuffer[k-1]=inbuffer[k];
      }
      inbuffer[offset+length_name-1]=0;
      this->name = (char *)(inbuffer + offset-1);
      offset += length_name;
      union {
        bool real;
        uint8_t base;
      } u_republish;
      u_republish.base = 0;
      u_republish.base |= ((uint8_t) (*(inbuffer + offset + 0))) << (8 * 0);
      this->republish = u_republish.real;
      offset += sizeof(this->republish);
     return offset;
    }

    const char * getType(){ return RECOGNIZEGAZEBOOBJECT; };
    const char * getMD5(){ return "9c648453b842979d1b130dac86a455cf"; };

  };

  class RecognizeGazeboObjectResponse : public ros::Msg
  {
    public:
      bool success;

    RecognizeGazeboObjectResponse():
      success(0)
    {
    }

    virtual int serialize(unsigned char *outbuffer) const
    {
      int offset = 0;
      union {
        bool real;
        uint8_t base;
      } u_success;
      u_success.real = this->success;
      *(outbuffer + offset + 0) = (u_success.base >> (8 * 0)) & 0xFF;
      offset += sizeof(this->success);
      return offset;
    }

    virtual int deserialize(unsigned char *inbuffer)
    {
      int offset = 0;
      union {
        bool real;
        uint8_t base;
      } u_success;
      u_success.base = 0;
      u_success.base |= ((uint8_t) (*(inbuffer + offset + 0))) << (8 * 0);
      this->success = u_success.real;
      offset += sizeof(this->success);
     return offset;
    }

    const char * getType(){ return RECOGNIZEGAZEBOOBJECT; };
    const char * getMD5(){ return "358e233cde0c8a8bcfea4ce193f8fc15"; };

  };

  class RecognizeGazeboObject {
    public:
    typedef RecognizeGazeboObjectRequest Request;
    typedef RecognizeGazeboObjectResponse Response;
  };

}
#endif
