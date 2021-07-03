from flask import Flask, render_template, request
import tracker

app = Flask(__name__)
tracker = tracker.FindSlot()
state_district_details = tracker.state_district_name


@app.route('/')
def home():
    return render_template('home.html', state_district_details=state_district_details)


@app.route('/pincode_availability', methods=['POST'])
def pincode_availability():
    if request.method == 'POST':

        pcode = str(request.form['pincode'])
        res, output = tracker.checkByPin(pcode)
        return render_template('pincode_availability.html', slotinfo=output, pincode=pcode)
    else:
        return render_template('pincode_availability.html', slotinfo="No slots available")


@app.route('/state_district_availability', methods=['POST'])
def state_district_availability():
    if request.method == 'POST':
        state = str(request.form['state'])
        district = str(request.form['districtselect'])
        res, output = tracker.checkByStateDistrict(state, district)
        return render_template('state_district_availability.html', slotinfo=output, state=state, district=district)
    else:
        return render_template('state_district_availability.html', slotinfo="No slots available")


if __name__ == "__main__":
    app.run(debug=False)
