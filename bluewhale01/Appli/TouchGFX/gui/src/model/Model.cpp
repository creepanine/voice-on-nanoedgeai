#include <gui/model/Model.hpp>
#include <gui/model/ModelListener.hpp>

extern "C"
{
extern void FaceDetect(void);
extern void EmoDetect(void);
}

Model::Model() : modelListener(0)
{

}

void Model::tick()
{
		tickCounter++;
		if((tickCounter%1000)==0)
		{
			FaceDetect();
			tickCounter=0;
		}

}
