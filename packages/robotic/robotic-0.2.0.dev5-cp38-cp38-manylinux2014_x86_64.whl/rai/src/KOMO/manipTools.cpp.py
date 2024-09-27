'''  ------------------------------------------------------------------
    Copyright (c) 2011-2024 Marc Toussaint
    email: toussaint@tu-berlin.de

    This code is distributed under the MIT License.
    Please see <root-path>/LICENSE for details.
    --------------------------------------------------------------  '''

#include "manipTools.h"

#include "../Optim/NLP_Solver.h"
#include "../Optim/NLP_Sampler.h"

ManipulationModelling.ManipulationModelling( str& _info)
  : info(_info)

ManipulationModelling.ManipulationModelling( std.shared_ptr<KOMO>& _komo)
  : komo(_komo)

def setup_inverse_kinematics(self, C, homing_scale, accumulated_collisions, joint_limits, quaternion_norms):  CHECK(not komo, "komo already given or previously setup")
  # setup a 1 phase single step problem
  komo = make_shared<KOMO>(C, 1., 1, 0, accumulated_collisions)
  komo.addControlObjective({}, 0, homing_scale)
  if accumulated_collisions:    komo.addObjective({}, FS_accumulatedCollisions, {}, OT_eq, {1e0})

  if joint_limits:    komo.addObjective({}, FS_jointLimits, {}, OT_ineq, {1e0})

  if quaternion_norms:    komo.addQuaternionNorms()



def setup_sequence(self, C, K, homing_scale, velocity_scale, accumulated_collisions, joint_limits, quaternion_norms):  CHECK(not komo, "komo already given or previously setup")
  komo = make_shared<KOMO>(C, double(K), 1, 1, accumulated_collisions)
  komo.addControlObjective({}, 0, homing_scale)
  komo.addControlObjective({}, 1, velocity_scale)
  if accumulated_collisions:    komo.addObjective({}, FS_accumulatedCollisions, {}, OT_eq, {1e0})

  if joint_limits:    komo.addObjective({}, FS_jointLimits, {}, OT_ineq, {1e0})

  if quaternion_norms:    komo.addQuaternionNorms()



def setup_motion(self, C, K, homing_scale, acceleration_scale, accumulated_collisions, joint_limits, quaternion_norms):  CHECK(not komo, "komo already given or previously setup")
  komo = make_shared<KOMO>(C, double(K), 16, 2, accumulated_collisions)
  if homing_scale>0.) komo.addControlObjective({}, 0, homing_scale:
  komo.addControlObjective({}, 2, acceleration_scale)
  if accumulated_collisions:    komo.addObjective({}, FS_accumulatedCollisions, {}, OT_eq, {1e0})

  if joint_limits:    komo.addObjective({}, FS_jointLimits, {}, OT_ineq, {1e0})

  if quaternion_norms:    komo.addQuaternionNorms()


  # zero vel at end
  komo.addObjective({double(K)}, FS_qItself, {}, OT_eq, {1e0}, {}, 1)


def setup_pick_and_place_waypoints(self, C, gripper, obj, homing_scale, velocity_scale, accumulated_collisions, joint_limits, quaternion_norms):  CHECK(not komo, "komo already given or previously setup")
  setup_sequence(C, 2, homing_scale, velocity_scale, accumulated_collisions, joint_limits, quaternion_norms)

  komo.addModeSwitch({1., -1.}, rai.SY_stable, {gripper, obj}, True)


def setup_point_to_point_motion(self, C, q0, q1, homing_scale, acceleration_scale, accumulated_collisions, quaternion_norms):  CHECK(not komo, "komo already given or previously setup")
  # setup a 1 phase fine-grained motion problem with 2nd order (acceleration) control costs
  komo = make_shared<KOMO>(C, 1., 32, 2, accumulated_collisions)
  komo.addControlObjective({}, 0, homing_scale)
  komo.addControlObjective({}, 2, acceleration_scale)
  komo.initWithWaypoints({q1}, 1, True, .5, 0)
  if accumulated_collisions:    komo.addObjective({}, FS_accumulatedCollisions, {}, OT_eq, {1e0})

  if quaternion_norms:    komo.addQuaternionNorms()


  # zero vel at end
  komo.addObjective({1.}, FS_qItself, {}, OT_eq, {1e0}, {}, 1)

  # end point
  komo.addObjective({1.}, FS_qItself, {}, OT_eq, {1e0}, q1)


def setup_point_to_point_rrt(self, C, q0, q1, explicitCollisionPairs):  rrt = make_shared<rai.PathFinder>()
  rrt.setProblem(C, q0, q1)
  if explicitCollisionPairs.N) rrt.setExplicitCollisionPairs(explicitCollisionPairs:


def add_helper_frame(self, type, parent, name, initFrame, rel, markerSize):  f = komo.addFrameDof(name, parent, type, True, initFrame, rel)
  if markerSize>0.:    f.setShape(rai.ST_marker, {.2})
    f.setColor({1., 0., 1.})

  if f.joint:    f.joint.sampleSdv=1.
    f.joint.setRandom(komo.timeSlices.d1, 0)



def grasp_top_box(self, time, gripper, obj, grasp_direction):  # grasp a box with a centered top grasp (axes fully aligned)
  rai.Array<FeatureSymbol> align
  if grasp_direction == "xz":    align = {FS_scalarProductXY, FS_scalarProductXZ, FS_scalarProductYZ
  } elif grasp_direction == "yz":    align = {FS_scalarProductYY, FS_scalarProductXZ, FS_scalarProductYZ
  } elif grasp_direction == "xy":    align = {FS_scalarProductXY, FS_scalarProductXZ, FS_scalarProductZZ
  } elif grasp_direction == "zy":    align = {FS_scalarProductXX, FS_scalarProductXZ, FS_scalarProductZZ
  } elif grasp_direction == "yx":    align = {FS_scalarProductYY, FS_scalarProductYZ, FS_scalarProductZZ
  } elif grasp_direction == "zx":    align = {FS_scalarProductYX, FS_scalarProductYZ, FS_scalarProductZZ
  } else:
    LOG(-2) <<"pickDirection not defined:" <<grasp_direction


  # position: centered
  komo.addObjective({time}, FS_positionDiff, {gripper, obj}, OT_eq, {1e1})

  # orientation: grasp axis orthoginal to target plane X-specific
  komo.addObjective({time-.2, time}, align(0), {obj, gripper}, OT_eq, {1e0})
  komo.addObjective({time-.2, time}, align(1), {obj, gripper}, OT_eq, {1e0})
  komo.addObjective({time-.2, time}, align(2), {obj, gripper}, OT_eq, {1e0})


def grasp_box(self, time, gripper, obj, palm, grasp_direction, margin):  # general grasp of a box, along provided grasp_axis (. 3
  # possible grasps of a box), and angle of grasp is decided by
  # inequalities on grasp plan and no-collision of box and palm
  arr xLine, yzPlane
  rai.Array<FeatureSymbol> align
  if grasp_direction == "x":    xLine = arr{1, 0, 0
    yzPlane = arr{{2, 3}, {0, 1, 0, 0, 0, 1}
    align = {FS_scalarProductXY, FS_scalarProductXZ
  } elif grasp_direction == "y":    xLine = arr{0, 1, 0
    yzPlane = arr{{2, 3}, {1, 0, 0, 0, 0, 1}
    align = {FS_scalarProductXX, FS_scalarProductXZ
  } elif grasp_direction == "z":    xLine = arr{0, 0, 1
    yzPlane = arr{{2, 3}, {1, 0, 0, 0, 1, 0}
    align = {FS_scalarProductXX, FS_scalarProductXY
  } else:
    LOG(-2) <<"grasp_direction not defined:" <<grasp_direction


  boxSize = komo.world.getFrame(obj).getSize();  boxSize.resizeCopy(3)
  boxSize.resizeCopy(3)

  # position: center in inner target plane X-specific
  komo.addObjective({time}, FS_positionRel, {gripper, obj}, OT_eq, xLine*1e1)
  komo.addObjective({time}, FS_positionRel, {gripper, obj}, OT_ineq, yzPlane*1e1, .5*boxSize-margin)
  komo.addObjective({time}, FS_positionRel, {gripper, obj}, OT_ineq, yzPlane*(-1e1), -.5*boxSize+margin)

  # orientation: grasp axis orthoginal to target plane X-specific
  komo.addObjective({time-.2, time}, align(0), {gripper, obj}, OT_eq, {1e0})
  komo.addObjective({time-.2, time}, align(1), {gripper, obj}, OT_eq, {1e0})

  # no collision with palm
  komo.addObjective({time-.3, time}, FS_distance, {palm, obj}, OT_ineq, {1e1}, {-.001})


def grasp_cylinder(self, time, gripper, obj, palm, margin):  # general grasp of a cylinder, squeezing the axis normally,
  # inequality along z-axis for positioning, no-collision with palm
  size = komo.world.getFrame(obj).getSize()

  # position: center along axis, within z-range
  komo.addObjective({time}, FS_positionRel, {gripper, obj}, OT_eq, arr{{2, 3}, {1, 0, 0, 0, 1, 0}}*1e1)
  komo.addObjective({time}, FS_positionRel, {gripper, obj}, OT_ineq, arr{0, 0, 1}*1e1, arr{0., 0., .5*size(0)-margin})
  komo.addObjective({time}, FS_positionRel, {gripper, obj}, OT_ineq, arr{0, 0, 1}*(-1e1), arr{0., 0., -.5*size(0)+margin})

  # orientation: grasp axis orthoginal to target plane X-specific
  komo.addObjective({time-.2, time}, FS_scalarProductXZ, {gripper, obj}, OT_eq, {1e0})

  # no collision with palm
  komo.addObjective({time-.3, time}, FS_distance, {palm, obj}, OT_ineq, {1e1}, {-.001})


#void ManipulationModelling.grasp_cylinder(double time, gripper, obj, palm, margin)#  size = komo.world[obj].getSize()

#  komo.addObjective({time}, FS_positionRel, {gripper, obj}, OT_eq, arr({2,3},{1,0,0,0,1,0})*1e1)
#  komo.addObjective({time}, FS_positionRel, {gripper, obj}, OT_ineq, arr({1,3},{0,0,1})*1e1, {0.,0.,.5*size(0)-margin})
#  komo.addObjective({time}, FS_positionRel, {gripper, obj}, OT_ineq, arr({1,3},{0,0,1})*(-1e1), {0.,0.,-.5*size(0)+margin})

#  # orientation: grasp axis orthoginal to target plane X-specific
#  komo.addObjective({time-.2,time}, FS_scalarProductXZ, {gripper, obj}, OT_eq, {1e0})

#  # no collision with palm
#  komo.addObjective({time-.3,time}, FS_negDistance, {palm, obj}, OT_ineq, {1e1}, {-.001})
#

#void ManipulationModelling.no_collision( arr& times, obj1, obj2, margin)#  komo.addObjective(times, FS_negDistance, {obj1, obj2}, OT_ineq, {1e1}, {-margin})
#

def place_box(self, time, obj, table, palm, place_direction, margin):  # placement of one box on another
  zVectorTarget = arr{0., 0., 1.
  boxSize = komo.world.getFrame(obj).getSize();  boxSize.resizeCopy(3)
  tableSize = komo.world.getFrame(table).getSize();  tableSize.resizeCopy(3)
  double relPos=0.
  FeatureSymbol zVector
  rai.Array<FeatureSymbol> align
  if place_direction == "x":    relPos = .5*(boxSize(0)+tableSize(2))
    zVector = FS_vectorX
    align = {FS_scalarProductXX, FS_scalarProductYX
  } elif place_direction == "y":    relPos = .5*(boxSize(1)+tableSize(2))
    zVector = FS_vectorY
    align = {FS_scalarProductXY, FS_scalarProductYY
  } elif place_direction == "z":    relPos = .5*(boxSize(2)+tableSize(2))
    zVector = FS_vectorZ
    align = {FS_scalarProductXZ, FS_scalarProductYZ
  } elif place_direction == "xNeg":    relPos = .5*(boxSize(0)+tableSize(2))
    zVector = FS_vectorX
    zVectorTarget *= -1.
    align = {FS_scalarProductXX, FS_scalarProductYX
  } elif place_direction == "yNeg":    relPos = .5*(boxSize(1)+tableSize(2))
    zVector = FS_vectorY
    zVectorTarget *= -1.
    align = {FS_scalarProductXY, FS_scalarProductYY
  } elif place_direction == "zNeg":    relPos = .5*(boxSize(2)+tableSize(2))
    zVector = FS_vectorZ
    zVectorTarget *= -1.
    align = {FS_scalarProductXZ, FS_scalarProductYZ
  } else:
    LOG(-2) <<"place_direction not defined:" <<place_direction


  # position: above table, table
  komo.addObjective({time}, FS_positionDiff, {obj, table}, OT_eq, 1e1*arr{{1, 3}, {0, 0, 1}}, arr{.0, .0, relPos})
  komo.addObjective({time}, FS_positionRel, {obj, table}, OT_ineq, 1e1*arr{{2, 3}, {1, 0, 0, 0, 1, 0}}, .5*tableSize-margin)
  komo.addObjective({time}, FS_positionRel, {obj, table}, OT_ineq, -1e1*arr{{2, 3}, {1, 0, 0, 0, 1, 0}}, -.5*tableSize+margin)

  # orientation: Z-up
  komo.addObjective({time-.2, time}, zVector, {obj}, OT_eq, {0.5}, zVectorTarget)
  komo.addObjective({time-.2, time}, align(0), {table, obj}, OT_eq, {1e0})
  komo.addObjective({time-.2, time}, align(1), {table, obj}, OT_eq, {1e0})

  # no collision with palm
  komo.addObjective({time-.3, time}, FS_distance, {palm, table}, OT_ineq, {1e1}, {-.001})


def straight_push(self, times, obj, gripper, table):  #start & end helper frames
  add_helper_frame(rai.JT_hingeZ, table, "_push_start", obj)
  add_helper_frame(rai.JT_transXYPhi, table, "_push_end", obj)

  #-- couple both frames symmetricaly
  #aligned orientation
  komo.addObjective({times(0)}, FS_vectorYDiff, {"_push_start", "_push_end"}, OT_eq, {1e1})
  #aligned position
  komo.addObjective({times(0)}, FS_positionRel, {"_push_end", "_push_start"}, OT_eq, 1e1*arr{{2, 3}, {1., 0., 0., 0., 0., 1.}})
  komo.addObjective({times(0)}, FS_positionRel, {"_push_start", "_push_end"}, OT_eq, 1e1*arr{{2, 3}, {1., 0., 0., 0., 0., 1.}})
  #at least 2cm appart, positivenot !not  direction
  komo.addObjective({times(0)}, FS_positionRel, {"_push_end", "_push_start"}, OT_ineq, -1e2*arr{{1, 3}, {0., 1., 0.}}, {.0, .02, .0})
  komo.addObjective({times(0)}, FS_positionRel, {"_push_start", "_push_end"}, OT_ineq, 1e2*arr{{1, 3}, {0., 1., 0.}}, {.0, -.02, .0})

  #gripper touch
  komo.addObjective({times(0)}, FS_negDistance, {gripper, obj}, OT_eq, {1e1}, {-.02})
  #gripper start position
  komo.addObjective({times(0)}, FS_positionRel, {gripper, "_push_start"}, OT_eq, 1e1*arr{{2, 3}, {1., 0., 0., 0., 0., 1.}})
  komo.addObjective({times(0)}, FS_positionRel, {gripper, "_push_start"}, OT_ineq, 1e1*arr{{1, 3}, {0., 1., 0.}}, {.0, -.02, .0})
  #gripper start orientation
  komo.addObjective({times(0)}, FS_scalarProductYY, {gripper, "_push_start"}, OT_ineq, {-1e1}, {.2})
  komo.addObjective({times(0)}, FS_scalarProductYZ, {gripper, "_push_start"}, OT_ineq, {-1e1}, {.2})
  komo.addObjective({times(0)}, FS_vectorXDiff, {gripper, "_push_start"}, OT_eq, {1e1})

  #obj end position
  komo.addObjective({times(1)}, FS_positionDiff, {obj, "_push_end"}, OT_eq, {1e1})
  #obj end orientation: unchanged
  komo.addObjective({times(1)}, FS_quaternion, {obj}, OT_eq, {1e1}, {}, 1); #qobjPose.rot.getArr4d())


def no_collision(self, time_interval, pairs, margin):  # inequality on distance between two objects
  _pairs = pairs.ref()
  _pairs.reshape(-1,2)
  for(uint i=0;i<_pairs.d0;i++)    komo.addObjective(time_interval, FS_negDistance, _pairs[i], OT_ineq, {1e1}, {-margin})



def switch_pick(self):  # a kinematic mode switch, obj becomes attached to gripper, freely parameterized but stable (=constant) relative pose


def switch_place(self):  # a kinematic mode switch, obj becomes attached to table, a 3D parameterized (XYPhi) stable relative pose
  # self requires obj and table to be boxes and assumes default placement alone z-axis
  # more general placements have to be modelled with switch_pick (table picking the object) and additinal user-defined geometric constraints


def target_position(self):  # impose a specific 3D target position on some object


def target_relative_xy_position(self, time, obj, relativeTo, pos):  # impose a specific 3D target position on some object
  if pos.N==2:    pos.append(0.)

  komo.addObjective({time}, FS_positionRel, {obj, relativeTo}, OT_eq, 1e1*arr{{2, 3}, {1, 0, 0, 0, 1, 0}}, pos)


def target_x_orientation(self, time, obj, x_vector):  komo.addObjective({time}, FS_vectorX, {obj}, OT_eq, {1e1}, x_vector)


def bias(self, time, qBias, scale):  # impose a square potential bias directly in joint space
  komo.addObjective({time}, FS_qItself, {}, OT_sos, {scale}, qBias)


def retract(self, time_interval, gripper, dist):  helper = STRING("_" <<gripper <<"_retract_" <<time_interval(0))
  t = conv_time2step(time_interval(0), komo.stepsPerPhase)
  pose = komo.timeSlices(komo.k_order+t, komo.world[gripper].ID).getPose()
  add_helper_frame(rai.JT_none, 0, helper, 0, pose)
#  komo.view(True, helper)

  komo.addObjective(time_interval, FS_positionRel, {gripper, helper}, OT_eq, * arr{{1, 3}, {1, 0, 0}})
  komo.addObjective(time_interval, FS_quaternionDiff, {gripper, helper}, OT_eq, {1e2})
  komo.addObjective({time_interval(1)}, FS_positionRel, {gripper, helper}, OT_ineq, -1e2 * arr{{1, 3}, {0, 0, 1}}, {0., 0., dist})


def approach(self, time_interval, gripper, dist):  helper = STRING("_" <<gripper <<"_approach_" <<time_interval(1))
  t = conv_time2step(time_interval(1), komo.stepsPerPhase)
  pose = komo.timeSlices(komo.k_order+t, komo.world[gripper].ID).getPose()
  add_helper_frame(rai.JT_none, 0, helper, 0, pose)
#  komo.view(True, helper)

  komo.addObjective(time_interval, FS_positionRel, {gripper, helper}, OT_eq, * arr{{1, 3}, {1, 0, 0}})
  komo.addObjective(time_interval, FS_quaternionDiff, {gripper, helper}, OT_eq, {1e2})
  komo.addObjective({time_interval(0)}, FS_positionRel, {gripper, helper}, OT_ineq, -1e2 * arr{{1, 3}, {0, 0, 1}}, {0., 0., dist})


def retractPush(self, time_interval, gripper, dist):  helper = STRING("_" <<gripper <<"_retractPush_"  <<time_interval(0))
  t = conv_time2step(time_interval(0), komo.stepsPerPhase)
  pose = komo.timeSlices(komo.k_order+t, komo.world[gripper].ID).getPose()
  add_helper_frame(rai.JT_none, 0, helper, 0, pose)
#  komo.addObjective(time_interval, FS_positionRel, {gripper, helper}, OT_eq, * arr{{1,3},{1,0,0}})
#  komo.addObjective(time_interval, FS_quaternionDiff, {gripper, helper}, OT_eq, {1e2})
  komo.addObjective(time_interval, FS_positionRel, {gripper, helper}, OT_eq, * arr{{1, 3}, {1, 0, 0}})
  komo.addObjective({time_interval(1)}, FS_positionRel, {gripper, helper}, OT_ineq, * arr{{1, 3}, {0, 1, 0}}, {0., -dist, 0.})
  komo.addObjective({time_interval(1)}, FS_positionRel, {gripper, helper}, OT_ineq, -1e2 * arr{{1, 3}, {0, 0, 1}}, {0., 0., dist})


def approachPush(self, time_interval, gripper, dist, _helper):#  if not helper.N) helper = STRING("_push_start":
#  komo.addObjective(time_interval, FS_positionRel, {gripper, helper}, OT_eq, * arr{{2,3},{1,0,0,0,0,1}})
#  komo.addObjective({time_interval(0)}, FS_positionRel, {gripper, helper}, OT_ineq, * arr{{1,3},{0,1,0}}, {0., -dist, 0.})
  helper = STRING("_" <<gripper <<"_approachPush_" <<time_interval(1))
  t = conv_time2step(time_interval(1), komo.stepsPerPhase)
  pose = komo.timeSlices(komo.k_order+t, komo.world[gripper].ID).getPose()
  add_helper_frame(rai.JT_none, 0, helper, 0, pose)
  komo.addObjective(time_interval, FS_positionRel, {gripper, helper}, OT_eq, * arr{{1, 3}, {1, 0, 0}})
  komo.addObjective({time_interval(0)}, FS_positionRel, {gripper, helper}, OT_ineq, * arr{{1, 3}, {0, 1, 0}}, {0., -dist, 0.})
  komo.addObjective({time_interval(0)}, FS_positionRel, {gripper, helper}, OT_ineq, -1e2 * arr{{1, 3}, {0, 0, 1}}, {0., 0., dist})


def solve(self, verbose):  if komo:    NLP_Solver sol
    sol.setProblem(komo.nlp())
    sol.opt.set_damping(1e-1). set_verbose(verbose-1). set_stopTolerance(1e-3). set_maxLambda(100.). set_stopInners(20). set_stopEvals(200)
    ret = sol.solve()
    if ret.feasible:      path = komo.getPath_qOrg()
    } else:
      path.clear()

    if not ret.feasible:      if verbose>0:        cout <<"  -- infeasible:" <<info <<"\n     " <<*ret <<endl
        if verbose>1:          cout <<sol.reportLagrangeGradients(komo.featureNames) <<endl
          cout <<komo.report(False, True, verbose>1) <<endl
          cout <<"  --" <<endl

        komo.view(True, STRING("infeasible: " <<info <<"\n" <<*ret))
        if verbose>2:          while(komo.view_play(True, 0, 1.))


    } else:
      if verbose>0:        cout <<"  -- feasible:" <<info <<"\n     " <<*ret <<endl
        if verbose>2:          cout <<sol.reportLagrangeGradients(komo.featureNames) <<endl
          cout <<komo.report(False, True, verbose>2) <<endl
          cout <<"  --" <<endl
          komo.view(True, STRING("feasible: " <<info <<"\n" <<*ret))
          if verbose>3:            while(komo.view_play(True, 0, 1.))





  } elif rrt:    rrt.rrtSolver.verbose=verbose
    ret = rrt.solve()
    if(ret.feasible) path = ret.x
    else path.clear()
  } else:
    NIY

  return path


def sample(self, sampleMethod, verbose):  CHECK(komo, "")

  NLP_Sampler sol(komo.nlp())
  arr data
  uintA dataEvals
  time = -rai.cpuTime()

#  sol.opt.seedMethod="gauss"
  if(sampleMethod) sol.opt.seedMethod=sampleMethod
  sol.opt.verbose=verbose
  sol.opt.downhillMaxSteps=50
  sol.opt.slackMaxStep=.5

  sol.run(data, dataEvals)
  time += rai.cpuTime()

  ret = make_shared<SolverReturn>()
  if data.N:    ret.x = data.reshape(-1)
    ret.evals = dataEvals.elem()
    ret.feasible = True
  }else:
    ret.evals = komo.evalCount
    ret.feasible = False

  ret.time = time
  ret.done = True
    totals = komo.info_errorTotals(komo.info_objectiveErrorTraces())
    ret.sos = totals(OT_sos)
    ret.ineq = totals(OT_ineq)
    ret.eq = totals(OT_eq)
    ret.f = totals(OT_f)


  if ret.feasible:    path = komo.getPath_qOrg()
  } else:
    path.clear()

  if not ret.feasible:    if verbose>0:      cout <<"  -- infeasible:" <<info <<"\n     " <<*ret <<endl
      if verbose>1:        cout <<komo.report(False, True, verbose>1) <<endl
        cout <<"  --" <<endl

      komo.view(True, STRING("infeasible: " <<info <<"\n" <<*ret))
      if verbose>2:        while(komo.view_play(True, 0, 1.))


  } else:
    if verbose>0:      cout <<"  -- feasible:" <<info <<"\n     " <<*ret <<endl
      if verbose>2:        cout <<komo.report(False, True, verbose>2) <<endl
        cout <<"  --" <<endl
        komo.view(True, STRING("feasible: " <<info <<"\n" <<*ret))
        if verbose>3:          while(komo.view_play(True, 0, 1.))





  return path


def debug(self, listObjectives, plotOverTime):  cout <<"  -- DEBUG: " <<info <<endl
  cout <<"  == solver return: " <<*ret <<endl
  cout <<"  == all KOMO objectives with increasing errors:\n" <<komo.report(False, listObjectives, plotOverTime) <<endl
#  cout <<"  == objectives sorted by error and Lagrange gradient:\n" <<sol.reportLagrangeGradients(komo.featureNames) <<endl
  cout <<"  == view objective errors over slices in gnuplot" <<endl
  cout <<"  == scroll through solution in display window using SHIFT-scroll" <<endl
  komo.view(True, STRING("debug: " <<info <<"\n" <<*ret))



def sub_motion(self, phase, homing_scale, acceleration_scale, accumulated_collisions, quaternion_norms):  rai.Configuration C
  arr q0, q1
  komo.getSubProblem(phase, C, q0, q1)

  std.shared_ptr<ManipulationModelling> manip = make_shared<ManipulationModelling>(STRING("sub_motion"<<phase))
  manip.setup_point_to_point_motion(C, q0, q1, homing_scale, acceleration_scale, accumulated_collisions, quaternion_norms)
  return manip


def sub_rrt(self, phase, explicitCollisionPairs):  rai.Configuration C
  arr q0, q1
  komo.getSubProblem(phase, C, q0, q1)

  std.shared_ptr<ManipulationModelling> manip = make_shared<ManipulationModelling>(STRING("sub_rrt"<<phase))
  manip.setup_point_to_point_rrt(C, q0, q1, explicitCollisionPairs)
  return manip


def play(self, C, duration):  dofIndices = C.getDofIDs()
  for(uint t=0; t<path.d0; t++)    C.setFrameState(komo.getConfiguration_X(t))
    C.setJointState(komo.getConfiguration_dofs(t, dofIndices))
    C.view(False, STRING("step " <<t <<"\n" <<info))
    rai.wait(duration/path.d0)




def addBoxPickObjectives(self, komo, time, dir, boxName, boxSize, gripperName, palmName, tableName, pre):  arr xLine, yzPlane
  FeatureSymbol xyScalarProduct=FS_none, xzScalarProduct=FS_none
  if dir==rai._xAxis:    xLine = arr{{1, 3}, {1, 0, 0}
    yzPlane = arr{{2, 3}, {0, 1, 0, 0, 0, 1}
    xyScalarProduct = FS_scalarProductXY
    xzScalarProduct = FS_scalarProductXZ
  } elif dir==rai._yAxis:    xLine = arr{{1, 3}, {0, 1, 0}
    yzPlane = arr{{2, 3}, {1, 0, 0, 0, 0, 1}
    xyScalarProduct = FS_scalarProductXX
    xzScalarProduct = FS_scalarProductXZ
  } elif dir==rai._zAxis:    xLine = arr{{1, 3}, {0, 0, 1}
    yzPlane = arr{{2, 3}, {1, 0, 0, 0, 1, 0}
    xyScalarProduct = FS_scalarProductXX
    xzScalarProduct = FS_scalarProductXY


  double margin=.02

  #position: center in inner target plane; X-specific
  if not pre:    komo.addObjective({time}, FS_positionRel, {gripperName, boxName}, OT_eq, xLine*1e1, {})
    komo.addObjective({time}, FS_positionRel, {gripperName, boxName}, OT_ineq, yzPlane*1e0, (boxSize/2.-margin))
    komo.addObjective({time}, FS_positionRel, {gripperName, boxName}, OT_ineq, yzPlane*(-1e0), -(boxSize/2.-margin))
  } else:
    komo.addObjective({time, time+1.}, FS_positionRel, {gripperName, boxName}, OT_eq, xLine*1e1, {})


  #orientation: grasp axis orthoginal to target plane; X-specific
  komo.addObjective({time-.2, time}, xyScalarProduct, {gripperName, boxName}, OT_eq, {1e0}, {})
  komo.addObjective({time-.2, time}, xzScalarProduct, {gripperName, boxName}, OT_eq, {1e0}, {})

  #no collision with palm
  if not pre:    komo.addObjective({time-.3, time}, FS_distance, {palmName, boxName}, OT_ineq, {1e1}, {-.001})
  } else:
    komo.addObjective({time-.3, time}, FS_distance, {palmName, boxName}, OT_eq, {1e1}, {-.07})


  #approach: only longitudial velocity, distance before and at grasp
  if komo.k_order>1) komo.addObjective({time-.3, time}, FS_positionRel, {boxName, gripperName}, OT_eq, arr{{2, 3}, {1, 0, 0, 0, 1, 0}}*1e2, {}, 1:
  if komo.k_order>1) komo.addObjective({time-.5, time-.3}, FS_distance, {palmName, boxName}, OT_ineq, {1e1}, {-.1}:

  #zero vel
  if komo.k_order>1) komo.addObjective({time}, FS_qItself, {}, OT_eq, {}, {}, 1:


void addBoxPlaceObjectives(KOMO& komo, time,
                           rai.ArgWord dir, boxName, boxSize,
                            char* tableName,
                            char* gripperName, palmName,
                           double margin, pre)  double relPos=0.
  zVector = FS_none
  zVectorTarget = {0., 0., 1.
  if dir==rai._xAxis:    relPos = .5*boxSize(0)+.03
    zVector = FS_vectorX
  } elif dir==rai._yAxis:    relPos = .5*boxSize(1)+.03
    zVector = FS_vectorY
  } elif dir==rai._zAxis:    relPos = .5*boxSize(2)+.03
    zVector = FS_vectorZ
  } elif dir==rai._xNegAxis:    relPos = .5*boxSize(0)+.03
    zVector = FS_vectorX
    zVectorTarget *= -1.
  } elif dir==rai._yNegAxis:    relPos = .5*boxSize(1)+.03
    zVector = FS_vectorY
    zVectorTarget *= -1.
  } elif dir==rai._zNegAxis:    relPos = .5*boxSize(2)+.03
    zVector = FS_vectorZ
    zVectorTarget *= -1.


  #z-position: fixed
  if not pre:    komo.addObjective({time}, FS_positionDiff, {boxName, tableName}, OT_eq, 1e1*arr({1, 3}, {0, 0, 1}), {.0, .0, relPos})
  } else:
    komo.addObjective({time}, FS_positionDiff, {boxName, tableName}, OT_eq, 1e1*arr({1, 3}, {0, 0, 1}), {.0, .0, relPos+.04})


  #xy-position: above table
  if not pre:    komo.addObjective({time}, FS_positionDiff, {boxName, tableName}, OT_eq, 1e1*arr({2, 3}, {1, 0, 0, 0, 1, 0}))
    #komo.addObjective({time}, FS_aboveBox, {boxName, tableName}, OT_ineq, {3e0}, {margin})
  } else:
    komo.addObjective({time}, FS_positionDiff, {boxName, tableName}, OT_eq, 1e1*arr({2, 3}, {1, 0, 0, 0, 1, 0}))
    #komo.addObjective({time, time+1.}, FS_aboveBox, {boxName, tableName}, OT_ineq, {3e0}, {margin})


  #orientation: Y-up
  komo.addObjective({time-.2, time}, zVector, {boxName}, OT_eq, {0.5}, zVectorTarget)

  #retract: only longitudial velocity, distance after grasp
  if komo.k_order>1) komo.addObjective({time, time+.3}, FS_positionRel, {boxName, gripperName}, OT_eq, arr{{2, 3}, {1, 0, 0, 0, 1, 0}}*1e2, {}, 1:
  if komo.k_order>1) komo.addObjective({time+.3, time+.5}, FS_distance, {palmName, boxName}, OT_ineq, {1e1}, {-.1}:

  #zero vel
  if komo.k_order>1) komo.addObjective({time}, FS_qItself, {}, OT_eq, {}, {}, 1:


