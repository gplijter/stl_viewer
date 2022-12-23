import vtk
import vtkmodules.util.colors

from pathlib import Path
import argparse

parser = argparse.ArgumentParser(
    prog='stlviewer_indirocknsole.exe',
    description='Program to visualize two soles')

parser.add_argument('-p_left', '--path_sole_left', type=str, help="path to the left sole")
parser.add_argument('-p_right', '--path_sole_right', type=str, help="path to the right sole")

args = parser.parse_args()

def getStlActor(fName):
    """ This imports a STL file"""
    reader = vtk.vtkSTLReader()
    reader.SetFileName(fName)

    """ The mapper is responsible for pushing the geometry into the graphics
        library. It may also do color mapping, if scalars or other
        attributes are defined."""
    mapper = vtk.vtkPolyDataMapper()
    # mapper = vtk.vtkOpenGLShaderProperty()
    mapper.SetInputConnection(reader.GetOutputPort())

    """ The LOD actor is a special type of actor. It will change appearance
       in order to render faster. At the highest resolution, it renders
       ewverything just like an actor. The middle level is a point cloud,
       and the lowest level is a simple bounding box."""
    actor = vtk.vtkLODActor()
    actor.GetProperty().SetColor(vtkmodules.util.colors.coral)
    # actor.GetProperty().SetColor(vtk)
    actor.SetMapper(mapper)
    return actor


def main():
    if args.path_sole_left is None or args.path_sole_left == "" or args.path_sole_right is None or args.path_sole_right == "":
        print ("please specify pathnames, see stlviewer_indirocknsole.exe -h for help")
        return None

    fNameLeft = Path(args.path_sole_left)
    fNameRight = Path(args.path_sole_right)

    # if len(sys.argv) > 1:
    #     fNameLeft = Path(sys.argv[1])
    #     fNameRight = Path(sys.argv[2])
    # else:
    #     raise BaseException("No path was given as input, please specify path to STL file")
    #     return None


    actor_left = getStlActor(fNameLeft)
    actor_right = getStlActor(fNameRight)
    actor_right.SetPosition(0.0, -150.0, 0.0)

    """ Create the graphics structure. The renderer renders into the render
        window. The render window interactor captures mouse events and will
        perform appropriate camera or actor manipulation depending on the
        nature of the events. """

    ren = vtk.vtkRenderer()

    renWin = vtk.vtkRenderWindow()
    # renWin.SetWindowName(f'STL Viewer - {fName.split("/")[-1]}')

    renWin.AddRenderer(ren)

    iren = vtk.vtkRenderWindowInteractor()
    iren.SetRenderWindow(renWin)

    vsty = vtk.vtkInteractorStyleTrackballCamera()
    iren.SetInteractorStyle(vsty)
    iren.SetRenderWindow(renWin)

    # Add the actors to the renderer, set the background and size
    ren.AddActor(actor_left)
    ren.AddActor(actor_right)
    ren.SetBackground(1.0, 1.0, 1.0)
    # self.renWin.SetSize(500, 500)

    # We'll zoom in a little by accessing the camera and invoking a "Zoom"
    # method on it.
    ren.ResetCamera()
    ren.GetActiveCamera().Zoom(0.8)
    ren.GetActiveCamera().SetPosition(-50, 650, 0)

    """ add an axes viewer"""
    ca = vtk.vtkCubeAxesActor()
    vbb = ren.ComputeVisiblePropBounds()
    ca.SetBounds(vbb)
    ca.SetCamera(ren.GetActiveCamera())

    c = (0.1, 0.1, 0.1)
    ca.GetXAxesLinesProperty().SetColor(c)
    ca.GetYAxesLinesProperty().SetColor(c)
    ca.GetZAxesLinesProperty().SetColor(c)
    for i in range(3):
        ca.GetLabelTextProperty(i).SetColor(c)
        ca.GetTitleTextProperty(i).SetColor(c)

    ca.XAxisLabelVisibilityOn()
    ca.YAxisLabelVisibilityOn()
    ca.ZAxisLabelVisibilityOn()

    ca.SetTitleOffset(3)
    ca.SetFlyMode(4)
    ca.SetXTitle("x (mm)")
    ca.SetYTitle("y (mm)")
    ca.SetZTitle("z (mm)")
    ca.PickableOff()
    ren.AddActor(ca)

    renWin.SetSize(renWin.GetScreenSize())
    renWin.Render()
    renWin.SetWindowName(f'STL Viewer')
    iren.Start()

if __name__ == '__main__':
    main()
