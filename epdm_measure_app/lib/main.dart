
import 'package:flutter/material.dart';
import 'package:intl/intl.dart';

void main() {
  runApp(EPDMMeasureApp());
}

class EPDMMeasureApp extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'EPDM Measure',
      theme: ThemeData(primarySwatch: Colors.blue),
      home: MeasureScreen(),
    );
  }
}

class MeasureScreen extends StatefulWidget {
  @override
  _MeasureScreenState createState() => _MeasureScreenState();
}

class _MeasureScreenState extends State<MeasureScreen> {
  final TextEditingController _speedController = TextEditingController();
  final TextEditingController _initialWeightController = TextEditingController();
  final TextEditingController _currentWeightController = TextEditingController();

  DateTime? _lastTopTime;
  double? _lastWeight;
  List<Map<String, dynamic>> _measures = [];

  void _recordTopTime() {
    final now = DateTime.now();
    final currentWeight = double.tryParse(_currentWeightController.text);
    if (_lastTopTime != null && _lastWeight != null && currentWeight != null) {
      final duration = now.difference(_lastTopTime!).inSeconds;
      final weightConsumed = _lastWeight! - currentWeight;
      final speed = double.tryParse(_speedController.text) ?? 1;
      final meters = speed * duration;
      final consumptionPerMeter = weightConsumed / meters;
      _measures.add({
        'time': DateFormat.Hms().format(now),
        'duration': duration,
        'weightConsumed': weightConsumed,
        'consumptionPerMeter': consumptionPerMeter,
      });
    }
    _lastTopTime = now;
    _lastWeight = currentWeight;
    setState(() {});
  }

  double _calculateAverageConsumption() {
    if (_measures.isEmpty) return 0;
    final validMeasures = _measures.map((m) => m['consumptionPerMeter']).whereType<double>().toList();
    if (validMeasures.isEmpty) return 0;
    return validMeasures.reduce((a, b) => a + b) / validMeasures.length;
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: Text('Mesure EPDM')),
      body: Padding(
        padding: const EdgeInsets.all(16.0),
        child: ListView(
          children: [
            TextField(
              controller: _speedController,
              keyboardType: TextInputType.number,
              decoration: InputDecoration(labelText: 'Vitesse de ligne (m/s)'),
            ),
            TextField(
              controller: _initialWeightController,
              keyboardType: TextInputType.number,
              decoration: InputDecoration(labelText: 'Poids initial de la palette (kg)'),
            ),
            TextField(
              controller: _currentWeightController,
              keyboardType: TextInputType.number,
              decoration: InputDecoration(labelText: 'Poids actuel (kg)'),
            ),
            SizedBox(height: 10),
            ElevatedButton(
              onPressed: _recordTopTime,
              child: Text('Enregistrer le top'),
            ),
            SizedBox(height: 20),
            Text('Mesures enregistrées:', style: TextStyle(fontWeight: FontWeight.bold)),
            ..._measures.map((m) => ListTile(
              title: Text('Top à ${m['time']}'),
              subtitle: Text('Durée: ${m['duration']}s, Consommation: ${m['consumptionPerMeter'].toStringAsFixed(4)} kg/m'),
            )),
            SizedBox(height: 20),
            Text('Consommation moyenne: ${_calculateAverageConsumption().toStringAsFixed(4)} kg/m'),
          ],
        ),
      ),
    );
  }
}
