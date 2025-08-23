import 'package:eventease/app/home/views/page/home.dart';
import 'package:eventease/core/router/routes.dart';
import 'package:go_router/go_router.dart';

class AppRouter {
  static GoRouter get routerData => GoRouter(
    initialLocation: '/',
    routes: <RouteBase>[
      ...homeBranch,
    ],
  );

  static List<RouteBase> get homeBranch {
    return [
      GoRoute(
        name: Routes.home.name,
        path: Routes.home.path,
        builder: (context, state) => HomePage(),
      ),
    ];
  }
}