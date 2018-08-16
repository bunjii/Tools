# Recorded script from Mayavi2
from numpy import array
try:
    engine = mayavi.engine
except NameError:
    from mayavi.api import Engine
    engine = Engine()
    engine.start()
if len(engine.scenes) == 0:
    engine.new_scene()
# ------------------------------------------- 
scene = engine.scenes[0]
scene.scene.do_render = True
scene.scene.do_render = True
scene.scene.do_render = True
scene.scene.do_render = True
scene.scene.do_render = True
scene.scene.do_render = True
scene.scene.do_render = True
scene.scene.do_render = True
scene.scene.do_render = True
scene.scene.do_render = True
scene.scene.do_render = True
scene.scene.do_render = True
glyph = engine.scenes[0].children[0].children[0].children[0]
glyph.glyph.glyph_source.glyph_source.angle = 72.1421245684502
scene.scene.do_render = True
glyph.glyph.glyph_source.glyph_source.center = array([ 0.,  0.,  0.])
scene.scene.do_render = True
glyph.glyph.glyph_source.glyph_source.direction = array([ 1.,  0.,  0.])
scene.scene.do_render = True
glyph.glyph.glyph_source.glyph_source.radius = 3.10386
scene.scene.do_render = True
glyph.glyph.glyph_source.glyph_source.angle = 0.0
scene.scene.do_render = True
glyph.glyph.glyph_source.glyph_source.center = array([ 0.,  0.,  0.])
scene.scene.do_render = True
glyph.glyph.glyph_source.glyph_source.direction = array([ 1.,  0.,  0.])
scene.scene.do_render = True
glyph.glyph.glyph_source.glyph_source.radius = 0.0
scene.scene.do_render = True
glyph.glyph.glyph_source.glyph_source.angle = 41.58584980739011
scene.scene.do_render = True
glyph.glyph.glyph_source.glyph_source.center = array([ 0.,  0.,  0.])
scene.scene.do_render = True
glyph.glyph.glyph_source.glyph_source.direction = array([ 1.,  0.,  0.])
scene.scene.do_render = True
glyph.glyph.glyph_source.glyph_source.radius = 0.8873999999999999
scene.scene.do_render = True
scene.scene.camera.position = [-0.35418024724716357, 3.2011052693695872, 2.1893937043718807]
scene.scene.camera.focal_point = [4.3811923503005747, 0.93780519769103854, -2.1602449814752429]
scene.scene.camera.view_angle = 30.0
scene.scene.camera.view_up = [0.19096994470696843, 0.94039022177865506, -0.28141910205547449]
scene.scene.camera.clipping_range = [0.016315766328485207, 16.315766328485207]
scene.scene.camera.compute_view_plane_normal()
scene.scene.render()
scene.scene.camera.position = [0.77042512906679117, 3.0630867300226483, 3.2166664025702345]
scene.scene.camera.focal_point = [4.3811923503005747, 0.93780519769103854, -2.1602449814752429]
scene.scene.camera.view_angle = 30.0
scene.scene.camera.view_up = [0.17259613128147369, 0.95015276048906749, -0.25965420697857605]
scene.scene.camera.clipping_range = [0.013663154463855093, 13.663154463855093]
scene.scene.camera.compute_view_plane_normal()
scene.scene.render()
glyph.glyph.glyph_source.glyph_source.center = array([ 0.,  0.,  0.])
scene.scene.do_render = True
glyph.glyph.glyph_source.glyph_source.direction = array([ 0.,  0.,  0.])
scene.scene.do_render = True
glyph.glyph.glyph_source.glyph_source.direction = array([ 0.,  0.,  0.])
scene.scene.do_render = True
glyph.glyph.glyph_source.glyph_source.center = array([ 0.,  0.,  0.])
scene.scene.do_render = True
glyph.glyph.glyph_source.glyph_source.direction = array([ 0.,  0.,  1.])
scene.scene.do_render = True
glyph.glyph.glyph_source.glyph_source.direction = array([ 0.,  0.,  1.])
scene.scene.do_render = True
scene.scene.camera.position = [0.54178526660354731, 3.3264592106071218, 2.9406297279957681]
scene.scene.camera.focal_point = [4.3811923503005747, 0.93780519769103854, -2.1602449814752429]
scene.scene.camera.view_angle = 30.0
scene.scene.camera.view_up = [0.19533262186864994, 0.93641999582994784, -0.29148371865982398]
scene.scene.camera.clipping_range = [0.014298930946026104, 14.298930946026104]
scene.scene.camera.compute_view_plane_normal()
scene.scene.render()
scene.scene.camera.position = [-0.26449022097282882, 3.8280765533194994, 4.0118134169846806]
scene.scene.camera.focal_point = [4.3811923503005747, 0.93780519769103854, -2.1602449814752429]
scene.scene.camera.view_angle = 30.0
scene.scene.camera.view_up = [0.19533262186864994, 0.93641999582994784, -0.29148371865982398]
scene.scene.camera.clipping_range = [0.015751883013266729, 15.751883013266729]
scene.scene.camera.compute_view_plane_normal()
scene.scene.render()
scene.scene.camera.position = [-1.2400835609402439, 4.435033538001476, 5.3079456806612653]
scene.scene.camera.focal_point = [4.3811923503005747, 0.93780519769103854, -2.1602449814752429]
scene.scene.camera.view_angle = 30.0
scene.scene.camera.view_up = [0.19533262186864994, 0.93641999582994784, -0.29148371865982398]
scene.scene.camera.clipping_range = [1.6627706971268212, 17.509955014627884]
scene.scene.camera.compute_view_plane_normal()
scene.scene.render()
scene.scene.camera.position = [-0.70073426037159958, 4.0994820210401013, 4.5913888928896629]
scene.scene.camera.focal_point = [4.3811923503005747, 0.93780519769103854, -2.1602449814752429]
scene.scene.camera.view_angle = 30.0
scene.scene.camera.view_up = [0.19533262186864994, 0.93641999582994784, -0.29148371865982398]
scene.scene.camera.clipping_range = [0.71477339180408039, 16.538018383413153]
scene.scene.camera.compute_view_plane_normal()
scene.scene.render()
scene.scene.camera.position = [-3.1373235933918004, 1.7036882087860714, 2.7684546038912723]
scene.scene.camera.focal_point = [4.3811923503005747, 0.93780519769103854, -2.1602449814752429]
scene.scene.camera.view_angle = 30.0
scene.scene.camera.view_up = [0.034992717730302179, 0.9942585973790723, -0.10112047885392511]
scene.scene.camera.clipping_range = [0.019938372205922299, 19.938372205922299]
scene.scene.camera.compute_view_plane_normal()
scene.scene.render()
glyph.glyph.glyph_source.glyph_source.center = array([ 0.,  0.,  0.])
scene.scene.do_render = True
glyph.glyph.glyph_source.glyph_source.direction = array([ 0.,  1.,  1.])
scene.scene.do_render = True
glyph.glyph.glyph_source.glyph_source.direction = array([ 0.,  1.,  1.])
scene.scene.do_render = True
glyph.glyph.glyph_source.glyph_source.center = array([ 0.,  0.,  0.])
scene.scene.do_render = True
glyph.glyph.glyph_source.glyph_source.direction = array([ 0.,  1.,  0.])
scene.scene.do_render = True
glyph.glyph.glyph_source.glyph_source.direction = array([ 0.,  1.,  0.])
scene.scene.do_render = True
glyph.glyph.glyph_source.glyph_source.center = array([ 0.,  0., -1.])
scene.scene.do_render = True
glyph.glyph.glyph_source.glyph_source.direction = array([ 0.,  1.,  0.])
scene.scene.do_render = True
glyph.glyph.glyph_source.glyph_source.center = array([ 0.,  0., -1.])
scene.scene.do_render = True
glyph.glyph.glyph_source.glyph_source.center = array([ 0.,  0.,  0.])
scene.scene.do_render = True
glyph.glyph.glyph_source.glyph_source.direction = array([ 0.,  1.,  0.])
scene.scene.do_render = True
glyph.glyph.glyph_source.glyph_source.center = array([ 0.,  0.,  0.])
scene.scene.do_render = True
glyph.glyph.glyph_source.glyph_source.center = array([ 0., -1.,  0.])
scene.scene.do_render = True
glyph.glyph.glyph_source.glyph_source.direction = array([ 0.,  1.,  0.])
scene.scene.do_render = True
glyph.glyph.glyph_source.glyph_source.center = array([ 0., -1.,  0.])
scene.scene.do_render = True
scene.scene.camera.position = [1.2555133977376782, 0.14613017466999381, 6.2665052894454725]
scene.scene.camera.focal_point = [4.3811923503005747, 0.93780519769103854, -2.1602449814752429]
scene.scene.camera.view_angle = 30.0
scene.scene.camera.view_up = [-0.072174765554203629, 0.99515779088967871, 0.066721619050874176]
scene.scene.camera.clipping_range = [3.1237059081612606, 12.471062754902587]
scene.scene.camera.compute_view_plane_normal()
scene.scene.render()
scene.scene.camera.position = [0.59912081769946912, -0.020121580164425779, 8.0361228463388237]
scene.scene.camera.focal_point = [4.3811923503005747, 0.93780519769103854, -2.1602449814752429]
scene.scene.camera.view_angle = 30.0
scene.scene.camera.view_up = [-0.072174765554203629, 0.99515779088967871, 0.066721619050874176]
scene.scene.camera.clipping_range = [4.9994978537779939, 14.394223183994495]
scene.scene.camera.compute_view_plane_normal()
scene.scene.render()
scene.scene.camera.position = [-0.19511420414676373, -0.22128620351407335, 10.177360090179778]
scene.scene.camera.focal_point = [4.3811923503005747, 0.93780519769103854, -2.1602449814752429]
scene.scene.camera.view_angle = 30.0
scene.scene.camera.view_up = [-0.072174765554203629, 0.99515779088967871, 0.066721619050874176]
scene.scene.camera.clipping_range = [7.2692061079742425, 16.721247303195696]
scene.scene.camera.compute_view_plane_normal()
scene.scene.render()
scene.scene.camera.position = [-1.5091142271034621, 5.3478589761042796, 8.8105474947521287]
scene.scene.camera.focal_point = [4.3811923503005747, 0.93780519769103854, -2.1602449814752429]
scene.scene.camera.view_angle = 30.0
scene.scene.camera.view_up = [0.074718931983186548, 0.938485991933244, -0.33713665500560303]
scene.scene.camera.clipping_range = [5.8226382118361215, 19.001809383357759]
scene.scene.camera.compute_view_plane_normal()
scene.scene.render()
scene.scene.camera.position = [-1.2924072870850316, 4.5008967766449386, 9.2673621845676681]
scene.scene.camera.focal_point = [4.5978992903190079, 0.090842998231697392, -1.7034302916596986]
scene.scene.camera.view_angle = 30.0
scene.scene.camera.view_up = [0.074718931983186548, 0.938485991933244, -0.33713665500560303]
scene.scene.camera.clipping_range = [5.8226382118361215, 19.001809383357759]
scene.scene.camera.compute_view_plane_normal()
scene.scene.render()
scene.scene.camera.position = [-2.5293716683398806, 5.4270080701117189, 11.571228604575415]
scene.scene.camera.focal_point = [4.5978992903190079, 0.090842998231697392, -1.7034302916596986]
scene.scene.camera.view_angle = 30.0
scene.scene.camera.view_up = [0.074718931983186548, 0.938485991933244, -0.33713665500560303]
scene.scene.camera.clipping_range = [8.5689851994135751, 21.817508567591219]
scene.scene.camera.compute_view_plane_normal()
scene.scene.render()
scene.scene.camera.position = [-1.8965560990840697, 6.0753145089712692, 11.650385279126574]
scene.scene.camera.focal_point = [5.2307148595748174, 0.73914943709124681, -1.6242736171085412]
scene.scene.camera.view_angle = 30.0
scene.scene.camera.view_up = [0.074718931983186548, 0.938485991933244, -0.33713665500560303]
scene.scene.camera.clipping_range = [8.5689851994135751, 21.817508567591219]
scene.scene.camera.compute_view_plane_normal()
scene.scene.render()
scene.scene.camera.position = [-2.9393080571088528, 7.0604068832081541, 10.573334658478279]
scene.scene.camera.focal_point = [5.2307148595748174, 0.73914943709124681, -1.6242736171085412]
scene.scene.camera.view_angle = 30.0
scene.scene.camera.view_up = [0.12750346154507469, 0.91292150293544672, -0.38770761763487283]
scene.scene.camera.clipping_range = [7.8265872292520999, 22.938314997977397]
scene.scene.camera.compute_view_plane_normal()
scene.scene.render()
scene.scene.camera.position = [-1.5213701955356536, 5.96332914462588, 8.4563943792442018]
scene.scene.camera.focal_point = [5.2307148595748174, 0.73914943709124681, -1.6242736171085412]
scene.scene.camera.view_angle = 30.0
scene.scene.camera.view_up = [0.12750346154507469, 0.91292150293544672, -0.38770761763487283]
scene.scene.camera.clipping_range = [5.0802402416746393, 20.122615813743938]
scene.scene.camera.compute_view_plane_normal()
scene.scene.render()
scene.scene.camera.position = [-2.1637074832304162, 5.756693104109333, 8.1332399819313768]
scene.scene.camera.focal_point = [4.5883775718800548, 0.53251339657470043, -1.9474280144213689]
scene.scene.camera.view_angle = 30.0
scene.scene.camera.view_up = [0.12750346154507469, 0.91292150293544672, -0.38770761763487283]
scene.scene.camera.clipping_range = [5.0802402416746393, 20.122615813743938]
scene.scene.camera.compute_view_plane_normal()
scene.scene.render()
scene.scene.camera.position = [-2.0547136143547582, 5.9031784888576819, 8.1286758664770211]
scene.scene.camera.focal_point = [4.5883775718800548, 0.53251339657470043, -1.9474280144213689]
scene.scene.camera.view_angle = 30.0
scene.scene.camera.view_up = [0.13309685785732089, 0.90836989816350666, -0.39642067874787879]
scene.scene.camera.clipping_range = [5.1265047626926101, 20.038375159871055]
scene.scene.camera.compute_view_plane_normal()
scene.scene.render()
