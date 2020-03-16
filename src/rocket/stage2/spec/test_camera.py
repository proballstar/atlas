try:
    from src import camera

except ImportError:
    print("Couldn't load Camera!")
    
def test_camera(mirror_status=True):
    camera.camera(mirror_status=mirror_status)